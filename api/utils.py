import json
import requests
from typing import Union, Tuple
from web3 import Web3

from .check_selfdestruct import might_selfdestruct


def analyze_contract(
    web3_interface: Web3, contract_address: str
) -> Tuple[bool, bool, bool]:
    """Check if a smart contract code hash has changed, contains metamorphic init code, or contains selfdestruct in the deployed code

    Args:
        rpc_endpoint (str): rpc endpoint for web3 interface
        contract_address (str): contract address that you want to check

    Returns:
        Tuple[bool, bool, bool]: code_hash_changed, is_metamorphic, contains_selfdestruct
    """

    deployment_block = find_deployment_block_for_contract(
        web3_interface, contract_address
    )
    print(deployment_block)
    code_hash_changed = check_code_hash_changed(
        web3_interface, contract_address, deployment_block
    )

    is_metamorphic, contains_selfdestruct = check_metamorphic_or_contains_selfdestruct(
        web3_interface, contract_address, deployment_block
    )

    return code_hash_changed, is_metamorphic, contains_selfdestruct


def find_deployment_block_for_contract(
    web3_interface: Web3, contract_address: str, latest_block: Union[int, None] = None
) -> int:
    """Find the deployment block for a contract

    Args:
        contract_address (str): contract address you want to find the deployment block for
        web3_interface (Web3): web3 interface
        latest_block (Union[int, str], optional): _description_. Defaults to None.

    Returns:
        int: the block number that this contract was deployed in
    """

    left = 0
    right = web3_interface.eth.getBlock(
        "latest" if not latest_block else latest_block
    ).number
    while True:
        if left == right:
            return left

        to_check = (left + right) // 2
        current_block = web3_interface.eth.get_code(
            contract_address, block_identifier=to_check
        )
        if len(current_block) == 0:
            left = to_check + 1
        else:
            right = to_check


def check_code_hash_changed(
    web3_interface: Web3, contract_address: str, deployment_block: int
) -> bool:
    """Check if the code hash of a contract changed between its deployment block and the latest block

    Args:
        web3_interface (Web3): web3 interface
        contract_address (str): contract address you want to check

    Returns:
        bool: has the contract code hash changed since deployment
    """

    deployment_code_hash = get_code_hash(
        web3_interface, contract_address, deployment_block
    )
    current_code_hash = get_code_hash(web3_interface, contract_address)

    return current_code_hash != deployment_code_hash


def get_code_hash(
    web3_interface: Web3, contract_address: str, block_number: int = None
) -> str:
    """Get code hash for a contract at a given block

    Args:
        web3_interface (Web3): web3 interface
        contract_address (str): contract address you want to check
        block_number (int, optional): the block number you want to check to code hash at. Defaults to None. If None, uses the latest block number

    Returns:
        str: code hash of the input contract at the given block number as a hex string
    """
    contract_code = web3_interface.eth.getCode(
        contract_address,
        block_identifier="latest" if not block_number else block_number,
    )

    return web3_interface.keccak(contract_code).hex()


def check_metamorphic_or_contains_selfdestruct(
    web3_interface: Web3, contract_address: str, block_number: int
) -> Tuple[bool, bool]:
    """Check if a contract was deployed with metamorphic init code described here
    https://github.com/0age/metamorphic/blob/master/contracts/MetamorphicContractFactory.sol

    Args:
        web3_interface (Web3): web3 interface
        contract_address (str): contract address that you want to check
        block_number (int): the deployment block for this contract

    Returns:
        bool: was this contract deployed with metamorphic init code
    """

    traces = web3_interface.provider.make_request("trace_block", [hex(block_number)])

    traces = traces.get("result")

    block_create_traces = [a for a in traces if "create" in a.get("type")]

    create_trace = [
        trace
        for trace in block_create_traces
        if trace.get("result").get("address") == contract_address.lower()
    ][0]

    init_code = create_trace.get("action").get("init")
    deployed_code = create_trace.get("result").get("code")

    is_metamorphic = contains_metamorphic_init_code(init_code)
    contains_selfdestruct = might_selfdestruct(deployed_code)

    return is_metamorphic, contains_selfdestruct


def contains_metamorphic_init_code(init_code: str) -> bool:
    """_summary_

    Args:
        init_code (str): _description_

    Returns:
        bool: _description_
    """
    metamorphic_init_code = (
        "0x5860208158601c335a63aaf10f428752fa158151803b80938091923cf3"
    )

    return metamorphic_init_code == init_code.lower()

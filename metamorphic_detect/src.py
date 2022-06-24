from time import sleep
from typing import Dict, Tuple, Union

from web3 import Web3

from .opcodes import contains_create2, contains_delegatecall, contains_selfdestruct
from .utils import validate_eth_address


def analyze_contract(
    web3_interface: Web3, contract_address: str
) -> Tuple[bool, bool, bool, bool, bool]:
    """Check if a smart contract code hash has changed, contains metamorphic init code, contains selfdestruct,
    or is deployed by another contract in the deployed code.

    Args:
        web3_interface (Web3): web3 interface
        contract_address (str): contract address that you want to check

    Returns:
        Tuple[bool, bool, bool, bool, bool, bool]:
                            code_hash_changed,
                            contains_metamorphic_init_code,
                            contains_selfdestruct,
                            contains_delegatecall,
                            deployed_by_contract,
                            deployer_contains_create2
    """

    if not validate_eth_address(contract_address):
        raise Exception("Invalid Ethereum Address")

    contract_address = web3_interface.toChecksumAddress(contract_address)

    deployment_block = find_deployment_block_for_contract(
        web3_interface, contract_address
    )

    create_trace = get_contract_creation_transaction_trace(
        web3_interface, contract_address, deployment_block
    )

    if create_trace is not None:
        deployer_address = web3_interface.toChecksumAddress(
            create_trace.get("action").get("from")
        )
        init_code = create_trace.get("action").get("init")
        runtime_code = create_trace.get("result").get("code")
        deployer_runtime_code = web3_interface.eth.getCode(deployer_address).hex()
        deployer_is_eoa = deployer_runtime_code == "0x"

        return (
            code_hash_changed(web3_interface, contract_address, deployment_block),
            contains_metamorphic_init_code(init_code),
            contains_selfdestruct(runtime_code),
            contains_delegatecall(runtime_code),
            not deployer_is_eoa,
            contains_create2(deployer_runtime_code),
        )

    else:
        return (False, False, False, False, False, False)


def find_deployment_block_for_contract(
    web3_interface: Web3, contract_address: str, latest_block: Union[int, None] = None
) -> int:
    """Find the deployment block for a contract

    Args:
        web3_interface (Web3): web3 interface
        contract_address (str): contract address you want to find the deployment block for
        latest_block (Union[int, str], optional): latest block number or "latest"

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


def get_contract_creation_transaction_trace(
    web3_interface: Web3, contract_address: str, deployment_block: int
) -> Union[Dict, None]:
    """Get a contract creation transaction trace init code and runtime/deployed code

    Args:
        web3_interface (Web3): web3 interface
        contract_address (str): contract address that you want to check
        deployment_block (int): the deployment block for this contract

    Returns:
        init_code (str): smart contract init code
        runtime_code (str): smart contract runtime or deployed code
    """
    retries = 3

    for i in range(retries):
        try:
            traces = web3_interface.provider.make_request(
                "trace_block", [hex(deployment_block)]
            )

            traces = traces.get("result")

            block_create_traces = [a for a in traces if a.get("type") == "create"]

            create_trace = [
                trace
                for trace in block_create_traces
                if trace.get("result").get("address") == contract_address.lower()
            ]

            if len(create_trace) > 0:
                return create_trace[0]
            else:
                return None
        except:
            if i < retries - 1:
                print("Alchemy request failed. Retrying request...")
                sleep(5)
                continue
            else:
                raise Exception(
                    "Alchemy request for transaction trace failed after 3 attempts. Please try again."
                )


def contains_metamorphic_init_code(init_code: str) -> bool:
    """Check if a contract was deployed with metamorphic init code described here
    https://github.com/0age/metamorphic/blob/master/contracts/MetamorphicContractFactory.sol

    Args:
        init_code (str): contract init code from contract creation/deployment transaction

    Returns:
        bool: was this contract deployed with metamorphic init code
    """
    return (
        "5860208158601c335a63aaf10f428752fa158151803b80938091923cf3"
        in init_code.lower()
    )


def code_hash_changed(
    web3_interface: Web3, contract_address: str, deployment_block: int
) -> bool:
    """Check if the code hash of a contract changed between its deployment block and the latest block

    Args:
        web3_interface (Web3): web3 interface
        contract_address (str): contract address you want to check
        deployment_block (int): the deployment block for this contract

    Returns:
        bool: has the contract code hash changed since deployment
    """
    deployment_block_code = web3_interface.eth.getCode(
        contract_address, block_identifier=deployment_block
    )

    deployment_block_code_hash = web3_interface.keccak(deployment_block_code).hex()

    current_block_code = web3_interface.eth.getCode(
        contract_address, block_identifier="latest"
    )
    current_block_code_hash = web3_interface.keccak(current_block_code).hex()

    return current_block_code_hash != deployment_block_code_hash

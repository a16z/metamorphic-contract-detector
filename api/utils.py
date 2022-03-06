import json
import requests
from typing import Union
from web3 import Web3




def is_metamorphic_contract(rpc_endpoint: str, contract_address: str) -> bool:
    """Check if a smart contract is a metamorphic contract

    Args:
        rpc_endpoint (str): rpc endpoint for web3 interface
        contract_address (str): contract address that you want to check

    Returns:
        bool: is the input contract address metamorphic or not
    """
    
    web3_interface = Web3(Web3.HTTPProvider(rpc_endpoint))
    
    deployment_block = find_deployment_block_for_contract(web3_interface, contract_address)

    code_hash_changed = check_code_hash_changed(web3_interface, contract_address, deployment_block)
    
    has_metamorphic_init_code = deployed_with_metamorphic_init_code(rpc_endpoint, contract_address, deployment_block)
    
    return has_metamorphic_init_code or code_hash_changed




def find_deployment_block_for_contract(
    web3_interface: Web3, contract_address: str, latest_block: Union[int, None]=None
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
    right = web3_interface.eth.get_block(
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




def check_code_hash_changed(web3_interface: Web3, contract_address: str, deployment_block: int) -> bool:
    """Check if the code hash of a contract changed between its deployment block and the latest block

    Args:
        web3_interface (Web3): web3 interface
        contract_address (str): contract address you want to check

    Returns:
        bool: has the contract code hash changed since deployment
    """
    
    deployment_code_hash = get_code_hash(web3_interface, contract_address, deployment_block)
    current_code_hash = get_code_hash(web3_interface, contract_address)

    return current_code_hash != deployment_code_hash




def get_code_hash(web3_interface: Web3, contract_address: str, block_number: int = None) -> str:
    """Get code hash for a contract at a given block

    Args:
        web3_interface (Web3): web3 interface
        contract_address (str): contract address you want to check
        block_number (int, optional): the block number you want to check to code hash at. Defaults to None. If None, uses the latest block number

    Returns:
        str: code hash of the input contract at the given block number as a hex string
    """
    contract_code = web3_interface.eth.get_code(
        contract_address,
        block_identifier = "latest" if not block_number else block_number
    )
    
    return web3_interface.keccak(contract_code).hex()




def deployed_with_metamorphic_init_code(rpc_endpoint: str, contract_address: str, block_number: int) -> bool:
    """Check if a contract was deployed with metamorphic init code described here
    https://github.com/0age/metamorphic/blob/master/contracts/MetamorphicContractFactory.sol

    Args:
        rpc_endpoint (str): rpc endpoint to query for block transaction traces
        contract_address (str): contract address that you want to check
        block_number (int): the deployment block for this contract

    Returns:
        bool: was this contract deployed with metamorphic init code
    """
    
    metamorphic_init_code = "0x5860208158601c335a63aaf10f428752fa158151803b80938091923cf3"

    headers = {"content-type":"application/json"}
    rpc_request_data = {
                "jsonrpc":"2.0",
                "id":0,
                "method":"trace_block",
                "params":[hex(block_number)]
            }

    res = requests.post(rpc_endpoint, headers = headers, data = json.dumps(rpc_request_data))
    res.raise_for_status()

    data = res.json()
    data = data.get("result")
    
    create_traces = [a for a in data if "create" in a.get("type")]
    
    for trace in create_traces:
        init_code = trace.get('action').get('init')
        created_address = trace.get('result').get('address')
        
        if created_address.lower() == contract_address.lower() and init_code.lower() == metamorphic_init_code:
            return True
        
    return False






    

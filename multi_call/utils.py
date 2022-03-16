from typing import List, Tuple
from web3 import Web3
from web3.eth import Contract
from eth_abi import decode_abi


def decode_func_outputs(
    contract: Contract, function_name: str, return_bytes: bytearray
) -> List:
    """Decode the returned bytes of a smart contract function call.

    Args:
        contract (Web3 Contract Object): Web3 Contract Object
        function_name (str): name of function you are trying to decode the output of
        return_bytes (bytearray): bytes returns from the smart contract function call

    Returns:
        List[Tuple]: List of decoded return data for each smart contract function call
    """

    func = contract.get_function_by_name(function_name)
    func_return_types = [
        return_type.get("type") for return_type in func.abi.get("outputs")
    ]
    return [decode_abi([*func_return_types], rb) for rb in return_bytes]


def eth_call(
    provider: Web3,
    payload: bytearray,
    return_types: List[str],
    block_identifier: int = 0,
) -> Tuple[int, bytearray]:
    """Execute an eth_all

    Args:
        provider (Web3): Web3 Provider Object
        payload (bytearray): input data to send in the eth_call

    Returns:
        Tuple[int,bytearray]: The blocknumber the eth_call is executed in and the returned data bytes
    """
    if block_identifier != 0:
        res = provider.eth.call(
            {"data": payload.hex()}, block_identifier=block_identifier
        )
    else:
        res = provider.eth.call({"data": payload.hex()})

    block_number, res_bytes = decode_abi(return_types, res)
    return block_number, res_bytes

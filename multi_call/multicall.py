from typing import Tuple
from web3 import Web3
from eth_abi import encode_abi
from .bytecode import CodeHash
from .utils import eth_call


def call_code_hash(provider: Web3, contract_address: str, block_identifer: int = 0) -> Tuple[int, bytes]:
     """[summary]

     Args:
         provider (Web3): [description]
         contract_address (str): [description]
         block_identifer (int, optional): [description]. Defaults to 0.

     Returns:
         Tuple[int, bytes]: [description]
     """
     input_data = encode_abi(['address'], [contract_address])
     full_payload = bytearray.fromhex(CodeHash.bytecode[2:]) + input_data

     block_number, res = eth_call(provider, full_payload, CodeHash.return_types, block_identifer)
     return block_number, res

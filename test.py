import requests
import os
import json
from web3 import Web3
from multi_call.multicall import call_code_hash
from api.utils import (
    get_deployment_txn,
    contains_metamorphic_deployment,
    find_deployment_block_for_contract,
    get_code_hash,
)
from dotenv import load_dotenv

load_dotenv("./.env")

RPC_ENDPOINT = os.getenv("A16Z_ALCHEMY_ENDPOINT")
web3 = Web3(Web3.HTTPProvider(RPC_ENDPOINT))


contract_address = web3.toChecksumAddress("0x000000009B988FbecFd83C55252f78592E609648")

# res = find_deployment_block_for_contract(web3, contract_address)

# res = get_code_hash(web3, contract_address)
# print(res)

# res = web3.eth.get_block(10639231)

# print(res)
METAMORPHIC_INIT_CODE = "0x5860208158601c335a63aaf10f428752fa158151803b80938091923cf3"
block_number = 10639231
contract_address = "0x000000009B988FbecFd83C55252f78592E609648"

headers = {"content-type": "application/json"}
data = {
    "jsonrpc": "2.0",
    "id": 0,
    "method": "trace_block",
    "params": [hex(block_number)],
}

res = requests.post(RPC_ENDPOINT, headers=headers, data=json.dumps(data))
res.raise_for_status()

data = res.json()
data = data.get("result")

create_traces = [a for a in data if "create" in a.get("type")]

for trace in create_traces:
    init_code = trace.get("action").get("init")
    created_address = trace.get("result").get("address")
    print(created_address, init_code)

    if (
        created_address.lower() == contract_address.lower()
        and init_code.lower() == METAMORPHIC_INIT_CODE
    ):
        print(True)

print(False)

c = "0x0000000000b92ac90d898eBa87fa5f2483f32234"
print()

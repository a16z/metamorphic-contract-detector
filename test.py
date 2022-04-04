from sre_constants import JUMP
import requests
import os
import json
from web3 import Web3

# from multi_call.multicall import call_code_hash
# from api.utils import (
#     get_deployment_txn,
#     contains_metamorphic_deployment,
#     find_deployment_block_for_contract,
#     get_code_hash,
# )
from dotenv import load_dotenv

load_dotenv()

RPC_ENDPOINT = os.getenv("RPC_ENDPOINT")
web3 = Web3(Web3.HTTPProvider(RPC_ENDPOINT))


contract_address = web3.toChecksumAddress("0xF1f640cdFBFa9A5b408c3D53282AD56e1C76FeF6")
# print(web3.eth.getTransactionCount(contract_address, block_identifier=	12437624	))
# proofFake = web3.eth.getProof(contract_address, positions = [1], block_identifier=	12605388		)
# print(proofFake['storageHash'])

# proofReal = web3.eth.getProof(contract_address, positions = [0], block_identifier=	11395644		)
# print(proofReal[ 'storageHash'])
# contract deployment nonce is 1

# res = find_deployment_block_for_contract(web3, contract_address)

# res = get_code_hash(web3, contract_address)
# print(res)

# res = web3.eth.get_block(10639231)

# print(res)
# METAMORPHIC_INIT_CODE = "0x5860208158601c335a63aaf10f428752fa158151803b80938091923cf3"
# block_number = 10639231
# contract_address = "0x000000009B988FbecFd83C55252f78592E609648"

# headers = {"content-type": "application/json"}
# data = {
#     "jsonrpc": "2.0",
#     "id": 0,
#     "method": "trace_block",
#     "params": [hex(block_number)],
# }

# res = requests.post(RPC_ENDPOINT, headers=headers, data=json.dumps(data))
# res.raise_for_status()

# data = res.json()
# data = data.get("result")

# create_traces = [a for a in data if "create" in a.get("type")]

# for trace in create_traces:
#     init_code = trace.get("action").get("init")
#     created_address = trace.get("result").get("address")
#     print(created_address, init_code)

#     if (
#         created_address.lower() == contract_address.lower()
#         and init_code.lower() == METAMORPHIC_INIT_CODE
#     ):
#         print(True)

# print(False)

# print()


STOP = 0x00
JUMPDEST = 0x5B
PUSH1 = 0x60
PUSH32 = 0x7F
RETURN = 0xF3
REVERT = 0xFD
INVALID = 0xFE
SELFDESTRUCT = 0xFF
HALTING = [STOP, RETURN, REVERT, INVALID, SELFDESTRUCT]

is_halting = lambda opcode: any([opcode == h for h in HALTING])
is_push = lambda opcode: opcode >= PUSH1 and opcode <= PUSH32


deployment_code = "341561000757005b63fa461e3360003560e01c14156100585761003260ac3560e81c60983560601c60843560601c610505565b61005661004a60243560043560043560ff1c15610465565b3360843560601c610759565b005b737dd6f92611a74612504bd8712a3ba3f2229095e733811461007957600080fd5b60003560f81c80156100ba5760018114610125576002811461017d5760038114610341576004811461035d5760058114610379576006811461039057600080fd5b6100cc60363560e01c43811490151790565b156101205760353560f81c156100e760253560801c826103eb565b6100f660253560801c8361040d565b915061010c60153560801c60013560601c610698565b61011d82823060013560601c6105c4565b50505b6103e4565b610137604a3560e01c43811490151790565b156101205760493560f81c1561015260393560801c826103eb565b61016160393560801c8361040d565b915061010c60293560801c60013560601c60153560601c610759565b60013560b81c60136002600a3560f81c14156101ae5750600f6101a8600b3560e01c43811490151790565b6101ae57005b8173c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25b36831015610309576101d73684610487565b60008280156101ed576001811461026d576102d2565b6001870135606090811c906015890135901c602989013560801c60398a013560f81c603a8b0161021e8383156103eb565b61022984841561040d565b925061023589836104c0565b9750600f8d1460138e141715610250576102508c878d610759565b61025c83828a896105c4565b509a509098509096506102d2915050565b6001870135606090811c906015890135901c602989013560e81c602c8a0161029587826104c0565b95508289106102b283858c6102a98561042c565b8f868d8c610616565b95509250819b508399506102c7838683610465565b6000039a5050505050505b5030811415610301577fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff850194505b5050506101c5565b506001600a3560f81c1415610339578083111561032557600080fd5b600b3560c01c838203101561033957600080fd5b5050506103e4565b61034c601535610808565b61012060153560013560601c61079d565b610366306107af565b801561037557610375816106ef565b5081ff5b61012060293560153560601c60013560601c610759565b60153560601c60293560601c6103ae60503560e01c43811490151790565b156103e1576103de603d3560e81c82846103c985871061042c565b60403560801c8688103060013560601c610616565b50505b50505b5050610856565b6000600182146001811461040157839150610406565b600091505b5092915050565b600060018214600181146104245760009150610406565b509192915050565b600060018214600181146104565773fffd8963efd1fc6a506488495d951d5263988d25915061045f565b6401000276a491505b50919050565b6000600182146001811461047b5784915061047f565b8391505b509392505050565b803560f81c60008180156104a257600181146104af576104b8565b84603a85011491506104b8565b84602c85011491505b509250929050565b600082600181146104fc57823560f81c80156104e357600181146104f2576104f6565b600184013560601c92506104f6565b3092505b50610406565b50309392505050565b8082838311156105155750829050815b600091825260208190526040859052606082207fff0000000000000000000000000000000000000000000000000000000000000083527f1f98431c8ad98523631ae4a59f267346ea31f9840000000000000000000000006001526015527fe34f199b19b2b4f47f68442619d555527d244f78a3297ea89325f843f87b8b546035526055822073ffffffffffffffffffffffffffffffffffffffff16913383146105bc578081fd5b505050505050565b60007f022c0d9f000000000000000000000000000000000000000000000000000000008152836004528460245282604452608060645280608452808160a48384865af161060f578081fd5b5050505050565b7f128acb08000000000000000000000000000000000000000000000000000000006000528160045282602452836044528460645260a0608452604060a4528560601b60c4528660601b60d8528760e81b60ec5260008061010460408182600080885af161068257600080fd5b5161012451909b909a5098505050505050505050565b60007fa9059cbb000000000000000000000000000000000000000000000000000000008152816004528260245280816044838473c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25af16106ea578081fd5b505050565b60007fa9059cbb000000000000000000000000000000000000000000000000000000008152737dd6f92611a74612504bd8712a3ba3f2229095e76004528160245280816044838473c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25af1610755578081fd5b5050565b60007fa9059cbb0000000000000000000000000000000000000000000000000000000081528260045283602452808160448384865af1610797578081fd5b50505050565b60008081828386865af16106ea578081fd5b7f70a0823100000000000000000000000000000000000000000000000000000000600052806004525060006020602480600073c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25afa61080157600080fd5b5060245190565b60007f2e1a7d4d0000000000000000000000000000000000000000000000000000000081528160045280816024838473c02aaa39b223fe8d0a0e5c4f27ead9083c756cc25af1610755578081fd5b"
deployment_code_bytes = bytearray.fromhex(deployment_code)

halted = False
i = 0

while i < len(deployment_code_bytes):

    opcode = deployment_code_bytes[i]

    if opcode == SELFDESTRUCT and not halted:
        print(True)
    elif opcode == JUMPDEST:
        halted = False
    elif is_halting(opcode):
        halted = True
    elif is_push(opcode):
        i += opcode - PUSH1 + 0x01
        continue

    i += 1

from collections import Counter

instructions = []
i = 0
while i < len(deployment_code_bytes):

    opcode = deployment_code_bytes[i]

    if is_push(opcode):
        instructions.append(hex(opcode))
        i += opcode - PUSH1 + 0x02
        continue
    else:
        if hex(opcode) == "0xff":
            print(i)
        instructions.append(hex(opcode))
        i += 1
print(Counter(instructions))
print(Counter(instructions)["0xff"])

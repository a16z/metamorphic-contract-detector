import re
import os
from web3 import Web3
from fastapi import FastAPI, HTTPException
from api.utils import analyze_contract
from dotenv import load_dotenv

load_dotenv()

RPC_ENDPOINT = os.getenv("RPC_ENDPOINT")

app = FastAPI()


@app.get("/ismetamorphic/{contract_address}")
def is_metamorphic(contract_address: str):

    regex_match = re.match(r"^0x[a-fA-F0-9]{40}$", contract_address)

    if regex_match == None:
        raise HTTPException(status_code=404, detail="Invalid Ethereum Address")

    web3_interface = Web3(Web3.HTTPProvider(RPC_ENDPOINT))

    code_hash_changed, is_metamorphic, contains_selfdestruct = analyze_contract(web3_interface, contract_address)

    return {"is_metamorphic": is_metamorphic}

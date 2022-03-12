import re
import os
from fastapi import FastAPI, HTTPException
from api.utils import is_metamorphic_contract
from dotenv import load_dotenv

load_dotenv()

RPC_ENDPOINT = os.getenv("RPC_ENDPOINT")

app = FastAPI()


@app.get("/ismetamorphic/{contract_address}")
def is_metamorphic(contract_address: str):

    regex_match = re.match(r"^0x[a-fA-F0-9]{40}$", contract_address)

    if regex_match == None:
        raise HTTPException(status_code=404, detail="Invalid Ethereum Address")

    is_metamorphic = is_metamorphic_contract(RPC_ENDPOINT, contract_address)

    return {"is_metamorphic": is_metamorphic}

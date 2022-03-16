from typing import Optional, List
from pydantic import BaseModel


class CallInput(BaseModel):
    target: str
    abi: List
    function: str
    args: List


class MultiCallContract(BaseModel):
    bytecode: str
    return_types: List[str]

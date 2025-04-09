from pydantic import BaseModel
from typing import List

class OptionContract(BaseModel):
    type: str
    strike: float
    expiration: str
    symbol: str

class OptionChainResponse(BaseModel):
    ticker: str
    contracts: List[OptionContract]

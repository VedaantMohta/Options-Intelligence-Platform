from pydantic import BaseModel
from typing import List, Literal

class OptionContract(BaseModel):
    type: str
    strike: float
    expiration: str
    symbol: str

class OptionChainResponse(BaseModel):
    ticker: str
    contracts: List[OptionContract]

class PricingRequest(BaseModel):
    S: float
    K: float
    T: float
    r: float
    sigma: float
    option_type: Literal["call", "put"]

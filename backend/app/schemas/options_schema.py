from pydantic import BaseModel, Field
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
    S: float = Field(..., gt=0, description="Current price of the underlying asset")
    K: float = Field(..., gt=0, description="Strike price of the option")
    T: float = Field(..., gt=0, description="Time to maturity in years")
    r: float = Field(..., ge=0, description="Annual risk-free interest rate")
    sigma: float = Field(..., gt=0, description="Annualized volatility of the underlying asset")
    option_type: Literal["call", "put"]
    model: Literal['black_scholes', 'binomial_tree'] = 'binomial_tree'
    steps: int = Field(100, gt=10, description="Number of steps for the Binomial Tree model")
    is_american: bool = True


class PricingResponse(BaseModel):
    price: float
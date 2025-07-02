from pydantic import BaseModel, Field
from typing import List, Literal, Optional

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

class OptionChainRequest(BaseModel):
    ticker: str
    option_type: Optional[str] = None
    expiration_date: Optional[str] = None
    min_strike_price: Optional[float] = None
    max_strike_price: Optional[float] = None

class PricedContract(BaseModel):
    symbol: str
    strike_price: float
    option_type: str
    expiration_date: str
    calculated_price: float

class PricedOptionChainResponse(BaseModel):
    ticker: str
    underlying_price: float
    volatility: float
    risk_free_rate: float
    priced_contracts: List[PricedContract]

class StrikesResponse(BaseModel):
    strikes: List[float]

# For the new GET /contract-details endpoint
class ContractDetailsResponse(BaseModel):
    underlying_price: float
    option_price: float
    volatility: float

# For the new POST /heatmap endpoint
class HeatmapRequest(BaseModel):
    ticker: str
    strike_price: float
    expiration_date: str
    option_type: Literal['call', 'put']

class HeatmapResponse(BaseModel):
    stock_price_axis: List[float]
    time_axis: List[float]
    prices: List[List[float]]
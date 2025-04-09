from fastapi import APIRouter, Query, HTTPException
from services.options_service import get_polygon_option_contracts

router = APIRouter()

@router.get("/")
def fetch_option_contracts(ticker: str = Query(..., description="Stock ticker symbol")):
    try:
        return get_polygon_option_contracts(ticker)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

from fastapi import FastAPI
from app.routers.options_router import router as options_router

app = FastAPI(
    title="Options Intelligence API",
    description="Quant-oriented backend for options analytics",
    version="0.1"
)

app.include_router(options_router, prefix="/options", tags=["Options"])

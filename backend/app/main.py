from fastapi import FastAPI

from app.api.breeze import router as breeze_router
from app.api.market import router as market_router
from app.api.risk import router as risk_router
from app.api.scanner import router as scanner_router
from app.api.watchlist import router as watchlist_router

app = FastAPI(
    title="Aura AI",
    description="AI Trading Assistant for Indian Markets",
    version="0.1.0",
) 

app.include_router(breeze_router)
app.include_router(market_router)
app.include_router(risk_router)
app.include_router(scanner_router)
app.include_router(watchlist_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Aura AI!",
        "status": "Running",
        "developer": "Shaurya Kedia"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
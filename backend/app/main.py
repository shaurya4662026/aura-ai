from fastapi import FastAPI

from app.api.breeze import router as breeze_router
from app.api.market import router as market_router
from app.api.risk import router as risk_router

app = FastAPI(
    title="Aura AI",
    description="AI Trading Assistant for Indian Markets",
    version="0.1.0",
) 

app.include_router(breeze_router)
app.include_router(market_router)
app.include_router(risk_router)


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
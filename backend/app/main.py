from fastapi import FastAPI

app = FastAPI(
    title="Aura AI",
    description="AI Trading Assistant for Indian Markets",
    version="0.1.0",
) 

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
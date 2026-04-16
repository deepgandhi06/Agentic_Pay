# main.py
from fastapi import FastAPI
import uvicorn
from api import router, set_model
from model_loader import load_model

app = FastAPI(title="ML Transaction Risk Service")

# Load ML model once
model = load_model()

# Inject model into API layer
set_model(model)

# Register routes
app.include_router(router)

if __name__ == "__main__":
    print("🚀 Starting ML Risk Service...")
    uvicorn.run(app, port=8003)


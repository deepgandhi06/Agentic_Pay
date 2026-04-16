from fastapi import FastAPI
from api.buyer_controller import router

app = FastAPI(title="AI Buyer Agent")

app.include_router(router)

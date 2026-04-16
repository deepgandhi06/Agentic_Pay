from fastapi import FastAPI
from api.controller import router
import threading
from start_idle_listener import start_idle_listener
import uvicorn
from log_store import logs



app = FastAPI(title="Invoice Agent")

app.include_router(router)

#logs = []

@app.on_event("startup")
def start_background_services():
    t = threading.Thread(target=start_idle_listener, daemon=True)
    t.start()

@app.get("/")
def health():
     return {"logs": logs}

    

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",   # IMPORTANT
        port=8002,        # Choose your port
        reload=True
    )


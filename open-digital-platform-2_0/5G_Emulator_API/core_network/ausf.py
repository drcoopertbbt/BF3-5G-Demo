# File location: 5G_Emulator_API/core_network/ausf.py
# File location: 5G_Emulator_API/core_network/ausf.py
from fastapi import FastAPI
import uvicorn
import requests
from contextlib import asynccontextmanager

nrf_url = "http://127.0.0.1:8000"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    nf_registration = {
        "nf_type": "AUSF",
        "ip": "127.0.0.1",
        "port": 9003
    }
    try:
        response = requests.post(f"{nrf_url}/register", json=nf_registration)
        response.raise_for_status()
        print("AUSF registered with NRF")
    except requests.RequestException as e:
        print(f"Failed to register AUSF with NRF: {str(e)}")
    
    yield
    # Shutdown
    # Add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)

@app.get("/ausf_service")
def ausf_service():
    return {"message": "AUSF service response"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9003)
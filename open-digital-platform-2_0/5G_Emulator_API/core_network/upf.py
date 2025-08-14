# File location: 5G_Emulator_API/core_network/upf.py
# File location: 5G_Emulator_API/core_network/upf.py
from fastapi import FastAPI
import uvicorn
import requests
from contextlib import asynccontextmanager

nrf_url = "http://127.0.0.1:8000"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    nf_registration = {
        "nf_type": "UPF",
        "ip": "127.0.0.1",
        "port": 9002
    }
    try:
        response = requests.post(f"{nrf_url}/register", json=nf_registration)
        response.raise_for_status()
        print("UPF registered with NRF")
    except requests.RequestException as e:
        print(f"Failed to register UPF with NRF: {str(e)}")
    
    yield
    # Shutdown
    # Add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)

@app.get("/upf_service")
def upf_service():
    return {"message": "UPF service response"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9002)
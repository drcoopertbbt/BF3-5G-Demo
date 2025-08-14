# File location: 5G_Emulator_API/ran/gnb.py
# File location: 5G_Emulator_API/ran/gnb.py
from fastapi import FastAPI, HTTPException
import uvicorn
import requests
import asyncio

app = FastAPI()
nrf_url = "http://127.0.0.1:8000"
amf_url = None

@app.on_event("startup")
async def register_with_nrf():
    global amf_url
    nf_registration = {
        "nf_type": "gNodeB",
        "ip": "127.0.0.1",
        "port": 38412
    }
    try:
        response = requests.post(f"{nrf_url}/register", json=nf_registration)
        response.raise_for_status()
        
        # Discover AMF
        amf_info = requests.get(f"{nrf_url}/discover/AMF").json()
        amf_url = f"http://{amf_info['ip']}:{amf_info['port']}"
    except requests.RequestException as e:
        print(f"Failed to register with NRF or discover AMF: {str(e)}")

@app.post("/initial_ue_message")
async def initial_ue_message(ue_data: dict):
    if not amf_url:
        raise HTTPException(status_code=503, detail="AMF not discovered")
    try:
        response = requests.post(f"{amf_url}/initial_ue_message", json=ue_data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send initial UE message: {str(e)}")

@app.get("/gnb_status")
async def gnb_status():
    return {"status": "operational", "amf_connected": amf_url is not None}

async def periodic_amf_heartbeat():
    while True:
        if amf_url:
            try:
                response = requests.get(f"{amf_url}/heartbeat")
                response.raise_for_status()
                print("AMF heartbeat successful")
            except requests.RequestException as e:
                print(f"AMF heartbeat failed: {str(e)}")
        await asyncio.sleep(60)  # Heartbeat every 60 seconds

@app.on_event("startup")
async def start_heartbeat():
    asyncio.create_task(periodic_amf_heartbeat())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=38412)
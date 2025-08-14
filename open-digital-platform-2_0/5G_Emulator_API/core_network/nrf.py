# File location: 5G_Emulator_API/core_network/nrf.py
# File location: 5G_Emulator_API/core_network/nrf.py
# File location: 5G_Emulator_API/core_network/nrf.py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class NFRegistration(BaseModel):
    nf_type: str
    ip: str
    port: int

nfs = {}

@app.post("/register")
def register_nf(nf: NFRegistration):
    nfs[nf.nf_type] = {"ip": nf.ip, "port": nf.port}
    return {"message": f"{nf.nf_type} registered successfully"}

@app.get("/discover/{nf_type}")
def discover_nf(nf_type: str):
    if nf_type in nfs:
        return nfs[nf_type]
    else:
        return {"message": f"{nf_type} not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

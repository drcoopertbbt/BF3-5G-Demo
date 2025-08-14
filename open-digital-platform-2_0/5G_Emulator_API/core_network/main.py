# File location: 5G_Emulator_API/core_network/main.py
# File location: 5G_Emulator_API/core_network/main.py
# File location: 5G_Emulator_API/core_network/main.py
import subprocess

def start_nf(file_path):
    subprocess.Popen(["python", file_path])

if __name__ == "__main__":
    # Start NRF
    start_nf("core_network/nrf.py")

    # Start Network Functions
    start_nf("core_network/amf.py")
    start_nf("core_network/smf.py")
    start_nf("core_network/upf.py")
    start_nf("core_network/ausf.py")
    start_nf("core_network/udm.py")
    
    # Start gNodeB
    start_nf("ran/gnb.py")

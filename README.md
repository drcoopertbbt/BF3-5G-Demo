# BF3-5G-Demo

![5G](https://img.shields.io/badge/5G%20Core-Network%20Emulator-blue.svg)
![Platform](https://img.shields.io/badge/platform-BlueField--3%20DPU-green.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)
![DOCA](https://img.shields.io/badge/DOCA%20SDK-2.6.0+-orange.svg)

> **Enterprise-grade 5G network emulation with NVIDIA BlueField-3 DPU integration**

A comprehensive 5G network simulation platform featuring complete core network emulation, RAN simulation, and **production-grade N6 interface firewall** powered by NVIDIA BlueField-3 DPUs with DOCA SDK.

---

## 🚀 Key Features

- **🏗️ Complete 5G Core Network**: AMF, SMF, UPF, NRF, AUSF, UDM, UDR, UDSF simulation
- **📡 RAN Simulation**: CU, DU, RRU components with realistic network behavior  
- **🛡️ N6 Interface Firewall**: Production-grade BlueField-3 DPU firewall with DOCA SDK
- **🔄 Hardware Acceleration**: Line-rate packet processing up to 400 Gbps
- **📊 Real-time Monitoring**: OpenTelemetry integration with comprehensive dashboards
- **🧪 Testing Framework**: Automated testing for all network components
- **⏱️ PTP Synchronization**: Precision Time Protocol for network synchronization

---

## ⚡ Quick Start

### Prerequisites
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%20LTS-orange.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![DOCA](https://img.shields.io/badge/DOCA%20SDK-2.6.0+-green.svg)

### Installation & Launch
```bash
# 1. Clone repository
git clone https://github.com/drcoopertbbt/BF3-5G-Demo.git
cd BF3-5G-Demo

# 2. Start 5G network emulation
cd open-digital-platform-2_0
pip install -r requirements.txt
python main.py

# 3. Test N6 interface firewall (BlueField-3 DPU)
cd open-digital-platform-2_0/n6-interface-simulation
./scripts/test_with_devemu.sh
```

---

## 📁 Project Structure

```bash
BF3-5G-Demo/
├── 🏗️ open-digital-platform-2_0/      # Complete 5G network simulation
│   ├── 5G_Emulator_API/              # Core 5G network functions
│   ├── n6-interface-simulation/      # BlueField-3 DPU firewall
│   ├── Dashboard/                    # Monitoring dashboards
│   └── main.py                       # Platform launcher
├── 📚 N6.md                          # N6 interface documentation
├── 🛡️ BF-Emulator.md                 # BlueField emulator guide
└── 📋 README.md                      # This file
```

---

## 🛡️ N6 Interface Firewall

### NEW: Production-Grade BlueField-3 DPU Integration
- **Hardware Acceleration**: DOCA Flow API integration
- **Line-Rate Processing**: Up to 400 Gbps throughput  
- **Real-time Security**: Advanced packet filtering and blocking
- **DevEmu Testing**: Complete hardware emulation for development

[📖 **Detailed N6 Firewall Documentation**](open-digital-platform-2_0/n6-interface-simulation/README.md)

### Demo Execution
```bash
# Complete N6 firewall validation
cd open-digital-platform-2_0/n6-interface-simulation
./scripts/test_with_devemu.sh
```

**Expected Results:**
- ✅ Baseline N6 connectivity validation
- 🔥 Firewall blocking demonstration  
- 📊 Real-time packet processing statistics

---

## 📊 Enterprise Features

### 5G Core Network Simulation
- **AMF**: Access and Mobility Management Function
- **SMF**: Session Management Function  
- **UPF**: User Plane Function
- **NRF**: Network Repository Function
- **AUSF**: Authentication Server Function
- **UDM/UDR**: Unified Data Management/Repository

### RAN Simulation
- **CU**: Central Unit with higher-layer protocols
- **DU**: Distributed Unit with real-time operations
- **RRU**: Remote Radio Unit simulation

### Monitoring & Observability
- **Real-time Dashboards**: System performance and metrics
- **OpenTelemetry Integration**: Comprehensive telemetry data
- **Performance Monitoring**: Throughput and latency analysis
- **Security Analytics**: Firewall events and blocked traffic

---

## 🏷️ Version Information

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Build](https://img.shields.io/badge/build-August%202024-green.svg)
![Platform](https://img.shields.io/badge/platform-Multi--Platform-orange.svg)

- **Version**: 2.0  
- **Build Date**: August 2024
- **5G Core**: Release 16/17 compliant
- **DOCA SDK**: 2.6.0+
- **Target Platforms**: x86_64, ARM64 (BlueField-3)

---

<div align="center">

**🌟 BF3-5G-Demo - Enterprise 5G Network Simulation with BlueField-3 DPU 🌟**

![5G](https://img.shields.io/badge/5G%20Core-Network%20Simulation-blue.svg)
![BlueField](https://img.shields.io/badge/BlueField--3-DPU%20Ready-green.svg)
![Enterprise](https://img.shields.io/badge/Enterprise-Grade-gold.svg)

**[📖 Complete Documentation](open-digital-platform-2_0/README.md)** | **[🛡️ N6 Firewall Guide](open-digital-platform-2_0/n6-interface-simulation/README.md)** | **[📋 N6 Interface Spec](N6.md)**

</div>

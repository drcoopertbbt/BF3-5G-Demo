# API Reference - 3GPP-Compliant 5G Network Simulator

## Overview

This document provides comprehensive API reference for all 5G Network Functions, organized by 3GPP interfaces and service categories. All endpoints follow 3GPP naming conventions where implemented.

## 3GPP Interface Map

```
                          5G Network Simulator API Endpoints
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          Service-Based Interface (SBI)                         │
│                                                                                 │
│  NRF Discovery & Registration              Core Network Services               │
│  ┌─────────────────────────┐               ┌─────────────────────────────────┐ │
│  │ POST /register          │               │ N11: Nsmf_PDUSession            │ │
│  │ GET  /discover/{nf}     │               │ N4:  PFCP Sessions              │ │
│  └─────────────────────────┘               │ N12: Nausf_UEAuthentication    │ │
│                                            │ N8:  Nudm_UECM                 │ │
│                                            └─────────────────────────────────┘ │
│                                                                                 │
│  User Plane & Data Services                RAN Interface Services             │
│  ┌─────────────────────────┐               ┌─────────────────────────────────┐ │
│  │ N6:  Data Network       │               │ N2:  NGAP Messages              │ │
│  │ N3:  GTP-U Tunneling    │               │ F1:  F1AP Protocol              │ │
│  │      Traffic Simulation │               │ Uu:  Radio Interface            │ │
│  └─────────────────────────┘               └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Core Network Functions APIs

### AMF (Access and Mobility Management Function)

**Base URL:** `http://localhost:9000`  
**3GPP Compliance Level:** 70% ✅ Good  
**Primary Interfaces:** N2, N11, N12

#### Endpoints

##### PDU Session Management (3GPP TS 29.502 Compliant)

```http
POST /amf/pdu-session/create
Content-Type: application/json

{
  "ue_id": "test_ue_001",
  "procedure": "pdu_session_establishment",
  "dnn": "internet",
  "sNssai": {
    "sst": 1,
    "sd": "010203"
  }
}
```

**Response:**
```json
{
  "status": "SUCCESS",
  "pduSessionId": 1,
  "message": "PDU Session established successfully",
  "smContextResponse": {
    "status": "CREATED",
    "ueIpAddress": "10.1.0.1",
    "n2SmInfo": {
      "pduSessionId": 1,
      "qosFlowSetupRequestList": [
        {
          "qfi": 9,
          "qosCharacteristics": {
            "5qi": 9,
            "priority": 80
          }
        }
      ]
    }
  }
}
```

##### UE Context Management

```http
POST /amf/ue/{ue_id}
Content-Type: application/json

{
  "imsi": "001010000000001",
  "supi": "imsi-001010000000001", 
  "pduSessionId": 1,
  "status": "registered",
  "location": {
    "tai": {
      "plmnId": {"mcc": "001", "mnc": "01"},
      "tac": "000001"
    }
  }
}
```

```http
GET /amf/ue/{ue_id}
```

##### NGAP Handover Procedures (3GPP TS 38.413)

```http
POST /amf/handover
Content-Type: application/json

{
  "ue_id": "test_ue_001",
  "source_gnb_id": "gnb001", 
  "target_gnb_id": "gnb002"
}
```

**Response:**
```json
{
  "message": "Handover process completed",
  "duration": 0.45
}
```

##### Monitoring & Metrics

```http
GET /metrics
```

**Response:**
```json
{
  "message": "Metrics are exposed on port 9100"
}
```

---

### SMF (Session Management Function)

**Base URL:** `http://localhost:9001`  
**3GPP Compliance Level:** 85% ✅ Excellent  
**Primary Interfaces:** N11, N4, N7

#### 3GPP-Compliant Service Endpoints (TS 29.502)

##### Nsmf_PDUSession Service

```http
POST /nsmf-pdusession/v1/sm-contexts
Content-Type: application/json

{
  "supi": "imsi-001010000000001",
  "pduSessionId": 1,
  "dnn": "internet",
  "sNssai": {
    "sst": 1,
    "sd": "010203"
  },
  "anType": "3GPP_ACCESS",
  "ratType": "NR",
  "ueLocation": {
    "nrLocation": {
      "tai": {
        "plmnId": {"mcc": "001", "mnc": "01"},
        "tac": "000001"
      },
      "ncgi": {
        "plmnId": {"mcc": "001", "mnc": "01"},
        "nrCellId": "000000001"
      }
    }
  },
  "gpsi": "msisdn-001010000000001"
}
```

**Response (TS 29.502 Compliant):**
```json
{
  "status": "CREATED",
  "cause": "PDU_SESSION_ESTABLISHMENT_ACCEPTED",
  "pduSessionId": 1,
  "ueIpAddress": "10.1.0.1",
  "n2SmInfo": {
    "pduSessionId": 1,
    "qosFlowSetupRequestList": [
      {
        "qfi": 9,
        "qosCharacteristics": {
          "5qi": 9,
          "priority": 80
        }
      }
    ],
    "n2InfoContent": "base64-encoded-ngap-pdu-session-resource-setup-request"
  },
  "smContext": {
    "contextId": "imsi-001010000000001:1",
    "ueIpAddress": "10.1.0.1"
  }
}
```

##### Session Management Status

```http
GET /smf/sessions
```

**Response:**
```json
{
  "activeSessions": 3,
  "sessions": [
    "imsi-001010000000001:1",
    "imsi-001010000000002:1", 
    "imsi-001010000000003:1"
  ]
}
```

##### Legacy Service Endpoint

```http
GET /smf_service
```

---

### UPF (User Plane Function)

**Base URL:** `http://localhost:9002`  
**3GPP Compliance Level:** 80% ✅ Good  
**Primary Interfaces:** N4, N3, N6

#### N4 Interface (PFCP Protocol - TS 29.244)

##### PFCP Session Management

```http
POST /n4/sessions
Content-Type: application/json

{
  "messageType": "PFCP_SESSION_ESTABLISHMENT_REQUEST",
  "seid": "smf-seid-1",
  "createPDR": [
    {
      "pdrId": 1,
      "precedence": 200,
      "pdi": {
        "sourceInterface": "ACCESS",
        "ueIpAddress": "10.1.0.1",
        "networkInstance": "internet"
      },
      "farId": 1
    }
  ],
  "createFAR": [
    {
      "farId": 1,
      "applyAction": "FORWARD",
      "forwardingParameters": {
        "destinationInterface": "CORE",
        "outerHeaderCreation": {
          "description": "GTP-U/UDP/IPv4",
          "teid": "1001"
        }
      }
    }
  ],
  "createQER": [
    {
      "qerId": 1,
      "qfi": 9,
      "uplinkMBR": 100000000,
      "downlinkMBR": 100000000
    }
  ]
}
```

**Response (TS 29.244 Compliant):**
```json
{
  "status": "SESSION_CREATED",
  "cause": "REQUEST_ACCEPTED", 
  "upfSeid": "upf-seid-a1b2c3d4",
  "n3_endpoint": "192.168.1.100",
  "createdPDR": [1],
  "createdFAR": [1],
  "createdQER": [1]
}
```

##### User Plane Traffic Simulation

```http
POST /upf/simulate-traffic
Content-Type: application/json

{
  "src_ip": "10.1.0.1",
  "dest_ip": "8.8.8.8",
  "packet_size": 1500,
  "protocol": "UDP"
}
```

**Response:**
```json
{
  "status": "FORWARDED",
  "packet_info": {
    "original": {
      "src_ip": "10.1.0.1",
      "dest_ip": "8.8.8.8",
      "packet_size": 1500,
      "protocol": "UDP"
    },
    "processed_via": "CORE",
    "tunnel_info": {
      "description": "GTP-U/UDP/IPv4",
      "teid": "1001"
    },
    "qos_applied": true
  }
}
```

##### Forwarding Rules Status

```http
GET /upf/forwarding-rules
```

**Response:**
```json
{
  "activeRules": 2,
  "activeSessions": 2,
  "rules": {
    "10.1.0.1": {
      "far": {
        "destinationInterface": "CORE",
        "outerHeaderCreation": {
          "description": "GTP-U/UDP/IPv4",
          "teid": "1001"
        }
      },
      "pdr_id": 1,
      "far_id": 1,
      "session_id": "smf-seid-1"
    }
  }
}
```

---

### NRF (Network Repository Function)

**Base URL:** `http://localhost:8000`  
**3GPP Compliance Level:** 30% ⚠️ Needs Enhancement  
**Primary Interfaces:** Service-Based Interface (SBI)

#### Service Registration & Discovery

##### NF Registration (Basic - Needs TS 29.510 Enhancement)

```http
POST /register
Content-Type: application/json

{
  "nf_type": "SMF",
  "ip": "127.0.0.1",
  "port": 9001
}
```

**Response:**
```json
{
  "message": "NF registered successfully"
}
```

**Required Enhancement (TS 29.510):**
```http
POST /nnrf-nfm/v1/nf-instances/{nfInstanceId}
Content-Type: application/json

{
  "nfInstanceId": "smf-001",
  "nfType": "SMF", 
  "nfStatus": "REGISTERED",
  "plmnList": [{"mcc": "001", "mnc": "01"}],
  "sNssais": [{"sst": 1, "sd": "010203"}],
  "nfServices": [
    {
      "serviceInstanceId": "nsmf-pdusession-001",
      "serviceName": "nsmf-pdusession",
      "versions": [{"apiVersionInUri": "v1"}],
      "scheme": "http",
      "nfServiceStatus": "REGISTERED"
    }
  ]
}
```

##### Service Discovery

```http
GET /discover/{nf_type}
```

**Example:**
```http
GET /discover/SMF
```

**Response:**
```json
{
  "nf_type": "SMF",
  "ip": "127.0.0.1", 
  "port": 9001
}
```

---

### AUSF (Authentication Server Function)

**Base URL:** `http://localhost:9003`  
**3GPP Compliance Level:** 10% ❌ Critical Implementation Needed  
**Primary Interfaces:** N12, N13

#### Current Implementation (Stub Only)

```http
GET /ausf_service
```

**Response:**
```json
{
  "message": "AUSF service response"
}
```

#### Required Implementation (TS 29.509)

**5G-AKA Authentication Request:**
```http
POST /nausf-auth/v1/ue-authentications
Content-Type: application/json

{
  "supiOrSuci": "imsi-001010000000001",
  "servingNetworkName": "5G:mnc001.mcc001.3gppnetwork.org",
  "resynchronizationInfo": {
    "rand": "base64-encoded-rand",
    "auts": "base64-encoded-auts"
  }
}
```

**Expected Response:**
```json
{
  "authType": "5G_AKA",
  "5gAuthData": {
    "rand": "base64-encoded-rand",
    "autn": "base64-encoded-autn", 
    "hxresstar": "base64-encoded-hxresstar"
  },
  "_links": {
    "5g-aka": {
      "href": "/nausf-auth/v1/ue-authentications/{authCtxId}/5g-aka-confirmation"
    }
  }
}
```

**Authentication Confirmation:**
```http
PUT /nausf-auth/v1/ue-authentications/{authCtxId}/5g-aka-confirmation
Content-Type: application/json

{
  "resStar": "base64-encoded-res-star"
}
```

---

### UDM (Unified Data Management)

**Base URL:** `http://localhost:9004`  
**3GPP Compliance Level:** 10% ❌ Critical Implementation Needed  
**Primary Interfaces:** N8, N10, N13

#### Current Implementation (Stub Only)

```http
GET /udm_service
```

#### Required Implementation (TS 29.503)

**Nudm_UECM - UE Context Management:**
```http
POST /nudm-uecm/v1/{supi}/registrations/amf-3gpp-access
Content-Type: application/json

{
  "amfInstanceId": "amf-001",
  "deregCallbackUri": "http://amf.example.com/callback",
  "guami": {
    "plmnId": {"mcc": "001", "mnc": "01"},
    "amfId": "000001"
  }
}
```

**Nudm_SDM - Subscriber Data Management:**
```http
GET /nudm-sdm/v1/{supi}/nssai?plmn-id={"mcc":"001","mnc":"01"}
```

**Expected Response:**
```json
{
  "defaultSingleNssais": [
    {"sst": 1, "sd": "010203"}
  ],
  "singleNssais": [
    {"sst": 1, "sd": "010203"},
    {"sst": 2, "sd": "020304"}
  ]
}
```

---

## RAN Components APIs

### gNodeB (5G Base Station)

**Base URL:** `http://localhost:9005`  
**3GPP Compliance Level:** 50% ⚠️ Needs Enhancement  
**Primary Interfaces:** N2, N3, Xn

#### Current Implementation

```http
GET /gnb_service
```

**Response:**
```json
{
  "message": "gNB service response"
}
```

#### Required Enhancement (TS 38.413)

**NGAP Initial UE Message:**
```http
POST /ngap/initial-ue-message
Content-Type: application/json

{
  "ran-ue-ngap-id": 1,
  "nas-pdu": "7e00410001",
  "user-location-information": {
    "nr-cgi": {
      "plmn-identity": "00101", 
      "nr-cell-identity": "000000001"
    },
    "tai": {
      "plmn-identity": "00101",
      "tac": "000001"  
    }
  },
  "rrc-establishment-cause": "mo-Data"
}
```

**UE Context Setup Response:**
```http
POST /ngap/ue-context-setup-response
Content-Type: application/json

{
  "amf-ue-ngap-id": 1,
  "ran-ue-ngap-id": 1,
  "pdu-session-resource-setup-response-list": [
    {
      "pdu-session-id": 1,
      "pdu-session-resource-setup-response-transfer": "base64-encoded-response"
    }
  ]
}
```

---

### CU/DU (Centralized/Distributed Units)

**Base URLs:** 
- CU: `http://localhost:9006`
- DU: `http://localhost:9007`

**3GPP Compliance Level:** 15% ❌ Critical Implementation Needed  
**Primary Interfaces:** F1, E1

#### Current Implementation (Stub Only)

```http
GET /cu_service  # CU
GET /du_service  # DU
```

#### Required Implementation (TS 38.463)

**F1 Setup Request (DU → CU):**
```http
POST /f1ap/setup-request
Content-Type: application/json

{
  "transaction-id": 1,
  "gnb-du-id": 1,
  "gnb-du-name": "DU-001",
  "served-cells-list": [
    {
      "served-cell-information": {
        "nr-cgi": {
          "plmn-identity": "00101",
          "nr-cell-identity": "000000001"
        },
        "nr-pci": 1,
        "five-gs-tac": "000001"
      }
    }
  ],
  "rrc-version": "rel16"
}
```

**F1 Setup Response (CU → DU):**
```http
POST /f1ap/setup-response  
Content-Type: application/json

{
  "transaction-id": 1,
  "gnb-cu-name": "CU-001",
  "cells-to-be-activated-list": [
    {
      "nr-cgi": {
        "plmn-identity": "00101", 
        "nr-cell-identity": "000000001"
      }
    }
  ]
}
```

---

## Supporting Services APIs

### N6 Interface & Data Network Simulation

**Base URLs:**
- UPF Service: `http://localhost:8081`
- DN Service: `http://localhost:8082`

#### N6 Interface Testing

```http
POST /upf/send-traffic
Content-Type: application/json

{
  "destination": "http://dn-service:8082/receive-traffic",
  "packet_count": 100,
  "packet_size": 1500,
  "interval_ms": 10
}
```

#### Data Network Simulation

```http
POST /dn/receive-traffic
Content-Type: application/json

{
  "source_ip": "10.1.0.1",
  "packet_data": "base64-encoded-packet",
  "timestamp": "2024-08-14T21:52:00Z"
}
```

---

## Error Codes and Status Responses

### HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful operation |
| 201 | Created | Resource created (e.g., PDU session) |
| 400 | Bad Request | Invalid request format |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |
| 502 | Bad Gateway | Upstream service error |

### 3GPP-Specific Error Codes

#### SMF Error Codes (TS 29.502)
```json
{
  "status": 400,
  "cause": "INVALID_REQUEST",
  "detail": "Missing mandatory field: supi",
  "invalidParams": [
    {
      "param": "supi",
      "reason": "Mandatory field missing"
    }
  ]
}
```

#### PFCP Error Codes (TS 29.244)
```json
{
  "status": "SESSION_ESTABLISHMENT_FAILED",
  "cause": "MANDATORY_IE_MISSING",
  "offendingIE": "PDR"
}
```

#### NGAP Error Codes (TS 38.413)
```json
{
  "procedureCode": 14,
  "criticality": "reject",
  "value": {
    "protocolIEs": {
      "cause": {
        "radioNetwork": "unspecified"
      }
    }
  }
}
```

---

## API Testing Examples

### cURL Examples

#### PDU Session Establishment Test
```bash
# 1. Create UE context
curl -X POST http://localhost:9000/amf/ue/test_ue_001 \
  -H "Content-Type: application/json" \
  -d '{
    "imsi": "001010000000001",
    "supi": "imsi-001010000000001",
    "pduSessionId": 1,
    "status": "registered"
  }'

# 2. Trigger PDU session establishment  
curl -X POST http://localhost:9000/amf/pdu-session/create \
  -H "Content-Type: application/json" \
  -d '{
    "ue_id": "test_ue_001",
    "procedure": "pdu_session_establishment",
    "dnn": "internet",
    "sNssai": {"sst": 1, "sd": "010203"}
  }'

# 3. Verify session state
curl -X GET http://localhost:9001/smf/sessions

# 4. Check UPF forwarding rules
curl -X GET http://localhost:9002/upf/forwarding-rules
```

#### Service Discovery Test
```bash
# Register NF with NRF
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "nf_type": "SMF",
    "ip": "127.0.0.1", 
    "port": 9001
  }'

# Discover SMF
curl -X GET http://localhost:8000/discover/SMF
```

### Python SDK Example

```python
import requests
import json

class FiveGSimulatorClient:
    def __init__(self, base_urls):
        self.amf_url = base_urls["amf"]
        self.smf_url = base_urls["smf"] 
        self.upf_url = base_urls["upf"]
        
    def establish_pdu_session(self, ue_id, dnn="internet"):
        """
        Establish PDU session following 3GPP procedure
        """
        # Step 1: Create UE context
        ue_context = {
            "imsi": f"00101000000000{ue_id[-3:]}",
            "supi": f"imsi-00101000000000{ue_id[-3:]}",
            "pduSessionId": 1,
            "status": "registered"
        }
        
        response = requests.post(
            f"{self.amf_url}/amf/ue/{ue_id}",
            json=ue_context
        )
        
        # Step 2: Trigger PDU session establishment
        session_request = {
            "ue_id": ue_id,
            "procedure": "pdu_session_establishment", 
            "dnn": dnn,
            "sNssai": {"sst": 1, "sd": "010203"}
        }
        
        response = requests.post(
            f"{self.amf_url}/amf/pdu-session/create",
            json=session_request
        )
        
        return response.json()

# Usage example
client = FiveGSimulatorClient({
    "amf": "http://localhost:9000",
    "smf": "http://localhost:9001", 
    "upf": "http://localhost:9002"
})

result = client.establish_pdu_session("test_ue_001")
print(f"PDU Session Result: {result}")
```

---

## OpenAPI Specification

For complete OpenAPI/Swagger specifications, the following files are generated:

- **AMF API**: `/docs/openapi/amf-api.yaml`
- **SMF API**: `/docs/openapi/smf-api.yaml` 
- **UPF API**: `/docs/openapi/upf-api.yaml`
- **NRF API**: `/docs/openapi/nrf-api.yaml`

Access interactive API documentation at:
- AMF: `http://localhost:9000/docs`
- SMF: `http://localhost:9001/docs`
- UPF: `http://localhost:9002/docs`

---

## Conclusion

This API reference provides comprehensive coverage of all implemented 3GPP-compliant endpoints. As components are enhanced to full 3GPP compliance, additional endpoints will be added following official specifications.

**Key Features:**
- 3GPP-compliant endpoint naming
- Standardized message formats
- Comprehensive error handling
- Complete testing examples
- OpenAPI documentation

**Enhancement Priorities:**
1. Complete AUSF/UDM API implementation
2. Full NRF NF Profile support
3. Enhanced NGAP message set
4. F1AP protocol implementation
import logging
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
import uvicorn
import requests
from contextlib import asynccontextmanager
import time
from typing import Dict
import json

# OpenTelemetry imports
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider, Span
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import start_http_server

# Create logs directory if it doesn't exist
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)

# Set up logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"{logs_dir}/amf_{timestamp}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Custom JSON File Exporter
class JsonFileExporter(SpanExporter):
    def __init__(self, file_path):
        self.file_path = file_path

    def export(self, spans):
        with open(self.file_path, 'a') as f:
            for span in spans:
                json.dump(self._span_to_dict(span), f)
                f.write('\n')
        return None

    def shutdown(self):
        pass

    def _span_to_dict(self, span: Span):
        return {
            "name": span.name,
            "context": {
                "trace_id": hex(span.context.trace_id),
                "span_id": hex(span.context.span_id),
            },
            "kind": span.kind.name,
            "start_time": span.start_time,
            "end_time": span.end_time,
            "status": {
                "status_code": span.status.status_code.name,
            },
            "attributes": dict(span.attributes),
            "events": [
                {
                    "name": event.name,
                    "timestamp": event.timestamp,
                    "attributes": dict(event.attributes),
                }
                for event in span.events
            ],
        }

# Set up tracing
resource = Resource.create({"service.name": "amf-service"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# File Exporter (Saves traces to a file)
trace_filename = f"{logs_dir}/trace_output_{timestamp}.json"
file_exporter = JsonFileExporter(trace_filename)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(file_exporter))

# Set up metrics
metric_reader = PrometheusMetricReader()
console_metric_exporter = ConsoleMetricExporter()
periodic_metric_reader = PeriodicExportingMetricReader(console_metric_exporter, export_interval_millis=5000)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader, periodic_metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

# Create metrics
handover_request_counter = meter.create_counter("ngap_handover_requests_total", description="Total number of NGAP Handover Requests")
handover_duration_histogram = meter.create_histogram("ngap_handover_duration_seconds", description="Duration of NGAP Handover process")

nrf_url = "http://127.0.0.1:8000"
smf_url = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global smf_url
    nf_registration = {
        "nf_type": "AMF",
        "ip": "0.0.0.0",
        "port": 9000
    }
    try:
        response = requests.post(f"{nrf_url}/register", json=nf_registration)
        response.raise_for_status()

        smf_info = requests.get(f"{nrf_url}/discover/SMF").json()
        if 'message' in smf_info:
            logger.error(f"SMF discovery failed: {smf_info['message']}")
        else:
            smf_url = f"http://{smf_info.get('ip')}:{smf_info.get('port')}"
            logger.info(f"SMF discovered at {smf_url}")
    except requests.RequestException as e:
        logger.error(f"Failed to register with NRF or discover SMF: {str(e)}")

    start_http_server(9100)
    yield

app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app)

# Simulated UE and gNB data
ue_contexts: Dict[str, Dict] = {}
gnb_data: Dict[str, Dict] = {
    "gnb001": {"ip": "192.168.1.1", "capacity": 100},
    "gnb002": {"ip": "192.168.1.2", "capacity": 100},
}

def handle_ngap_handover_request(request_data: Dict):
    with tracer.start_as_current_span("ngap_handover_request") as span:
        span.set_attribute("ngap.message_type", "NGAP_HANDOVER_REQUEST")
        span.set_attribute("ngap.source_gnb_id", request_data['source_gnb_id'])
        
        logger.info(f"Handling NGAP Handover Request for UE: {request_data['ue_id']} from source gNB: {request_data['source_gnb_id']}")
        
        # Simulate processing of handover request
        ue_id = request_data['ue_id']
        if ue_id not in ue_contexts:
            logger.error(f"UE context for {ue_id} not found!")
            raise HTTPException(status_code=404, detail="UE context not found")
        
        # Decide on target gNB (simplified logic)
        target_gnb_id = "gnb002" if request_data['source_gnb_id'] == "gnb001" else "gnb001"
        logger.info(f"Decided target gNB for UE {ue_id}: {target_gnb_id}")
        
        # Update UE context
        ue_contexts[ue_id]['target_gnb_id'] = target_gnb_id
        
        # Simulate sending NGAP Handover Request Acknowledge
        send_ngap_handover_request_ack(request_data['source_gnb_id'])
        
        return target_gnb_id

def send_ngap_handover_request_ack(source_gnb_id: str):
    with tracer.start_as_current_span("ngap_handover_request_ack") as span:
        span.set_attribute("ngap.message_type", "NGAP_HANDOVER_REQUEST_ACK")
        span.set_attribute("ngap.source_gnb_id", source_gnb_id)
        logger.info(f"Sending NGAP Handover Request Acknowledge to source gNB: {source_gnb_id}")
        # Simulate sending acknowledgment
        time.sleep(0.01)  # Simulate network delay

def initiate_ngap_resource_setup(target_gnb_id: str):
    with tracer.start_as_current_span("ngap_resource_setup") as span:
        span.set_attribute("ngap.message_type", "NGAP_RESOURCE_SETUP_REQUEST")
        span.set_attribute("ngap.target_gnb_id", target_gnb_id)
        
        logger.info(f"Initiating resource setup for target gNB: {target_gnb_id}")
        
        # Simulate sending resource setup request to target gNB
        time.sleep(0.02)  # Simulate network delay
        logger.info(f"Resource setup request sent to {target_gnb_id}")
        
        # Simulate receiving resource setup response
        time.sleep(0.02)  # Simulate network delay
        logger.info(f"Resource setup response received from {target_gnb_id}")
        
        span.add_event("Resource setup completed")

def send_ngap_handover_command(source_gnb_id: str, target_gnb_id: str):
    with tracer.start_as_current_span("ngap_handover_command") as span:
        span.set_attribute("ngap.message_type", "NGAP_HANDOVER_COMMAND")
        span.set_attribute("ngap.source_gnb_id", source_gnb_id)
        span.set_attribute("ngap.target_gnb_id", target_gnb_id)
        
        logger.info(f"Sending NGAP Handover Command from source gNB: {source_gnb_id} to target gNB: {target_gnb_id}")
        
        # Simulate sending handover command to source gNB
        time.sleep(0.01)  # Simulate network delay
        
        # Wait for handover complete message
        time.sleep(0.03)  # Simulate handover execution time
        span.add_event("Handover completed")
        logger.info(f"Handover completed for UE at target gNB: {target_gnb_id}")

@app.post("/amf/handover")
async def amf_handover(request_data: Dict):
    start_time = time.time()
    handover_request_counter.add(1)
    
    try:
        # Simulate receiving NGAP Handover Request
        target_gnb_id = handle_ngap_handover_request(request_data)
        
        # Simulate NGAP Resource Setup
        initiate_ngap_resource_setup(target_gnb_id)
        
        # Simulate sending NGAP Handover Command
        send_ngap_handover_command(request_data['source_gnb_id'], target_gnb_id)
        
        # Record handover duration
        duration = time.time() - start_time
        handover_duration_histogram.record(duration)
        
        logger.info(f"Handover process completed in {duration} seconds")
        return {"message": "Handover process completed", "duration": duration}
    except Exception as e:
        logger.error(f"Handover failed: {str(e)}")
        return {"message": f"Handover failed: {str(e)}"}

@app.get("/amf/ue/{ue_id}")
async def get_ue_context(ue_id: str):
    if ue_id not in ue_contexts:
        raise HTTPException(status_code=404, detail="UE context not found")
    return ue_contexts[ue_id]

@app.post("/amf/ue/{ue_id}")
async def create_ue_context(ue_id: str, context: Dict):
    ue_contexts[ue_id] = context
    logger.info(f"UE context created for {ue_id}")
    return {"message": "UE context created"}

@app.get("/metrics")
async def metrics():
    return {"message": "Metrics are exposed on port 9100"}

if __name__ == "__main__":
    logger.info("Starting AMF service")
    uvicorn.run(app, host="0.0.0.0", port=9000)
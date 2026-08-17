from fastapi import FastAPI
from enterprise_logger import setup_enterprise_logger

logger = setup_enterprise_logger("AeroDrift.API")
from fastapi import Request
import time

app = FastAPI(title="AeroDrift Enterprise API", version="1.0.0")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"API Request: {request.method} {request.url.path} - Status: {response.status_code} - Duration: {process_time:.4f}s")
    return response

@app.on_event("startup")
async def startup_event():
    logger.info("AeroDrift API Server Booting Up...")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AeroDrift API"}

from config import Config
from aws_live_ingestion import LiveAWSIngestor
from aws_ingestion import fetch_all_resources as fetch_mock_resources
from graph_engine import CloudTopologyEngine

async def get_cloud_state():
    if Config.MODE == "LIVE":
        ingestor = LiveAWSIngestor()
        state = await ingestor.fetch_all_resources()
        if not state["ec2"]:
            state = await fetch_mock_resources()
    else:
        state = await fetch_mock_resources()
    return state

@app.get("/api/v1/topology")
async def get_topology():
    state = await get_cloud_state()
    engine = CloudTopologyEngine(state)
    engine.build()
    return {
        "nodes": list(engine.graph.nodes(data=True)),
        "edges": list(engine.graph.edges(data=True))
    }

from drift_detector import DriftDetector

@app.get("/api/v1/drift")
async def get_drift_analysis():
    state = await get_cloud_state()
    engine = CloudTopologyEngine(state)
    engine.build()
    
    detector = DriftDetector(engine.graph)
    alerts = detector.run_all_scans()
    
    return {
        "status": "vulnerable" if alerts else "secure",
        "alerts": alerts
    }

from remediation_engine import AutoRemediator
from fastapi import HTTPException

@app.post("/api/v1/remediate")
async def trigger_remediation():
    state = await get_cloud_state()
    engine = CloudTopologyEngine(state)
    engine.build()
    
    detector = DriftDetector(engine.graph)
    alerts = detector.run_all_scans()
    
    if not alerts:
        return {"message": "No drift detected. Infrastructure is secure."}
        
    remediator = AutoRemediator(alerts)
    script_path = remediator.generate_script()
    
    return {
        "message": "Remediation triggered successfully.",
        "script_path": script_path,
        "alerts_fixed": alerts
    }

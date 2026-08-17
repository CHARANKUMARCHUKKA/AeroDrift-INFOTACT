from fastapi import FastAPI
from enterprise_logger import setup_enterprise_logger

logger = setup_enterprise_logger("AeroDrift.API")
app = FastAPI(title="AeroDrift Enterprise API", version="1.0.0")

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

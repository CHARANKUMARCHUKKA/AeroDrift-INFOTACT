from fastapi import FastAPI
from enterprise_logger import setup_enterprise_logger

logger = setup_enterprise_logger("AeroDrift.API")
from fastapi import Request
import time

app = FastAPI(title="AeroDrift Enterprise API", version="1.0.0")

from database import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

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
from aws_ingestion import ingest_cloud_state as fetch_mock_resources
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

import json

@app.get("/api/v1/drift")
async def get_drift_analysis(db: Session = Depends(get_db)):
    state = await get_cloud_state()
    engine = CloudTopologyEngine(state)
    engine.build()
    
    detector = DriftDetector(engine.graph)
    alerts = detector.run_all_scans()
    
    scan_status = "vulnerable" if alerts else "secure"
    
    # Save to database
    db_log = models.SecurityScanLog(
        status=scan_status,
        alerts_detected=json.dumps(alerts)
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    return {
        "scan_id": db_log.id,
        "status": scan_status,
        "alerts": alerts
    }

from remediation_engine import AutoRemediator
from fastapi import HTTPException

@app.post("/api/v1/remediate")
async def trigger_remediation(db: Session = Depends(get_db)):
    state = await get_cloud_state()
    engine = CloudTopologyEngine(state)
    engine.build()
    
    detector = DriftDetector(engine.graph)
    alerts = detector.run_all_scans()
    
    if not alerts:
        return {"message": "No drift detected. Infrastructure is secure."}
        
    remediator = AutoRemediator(alerts)
    script_path = remediator.generate_script()
    
    # Mark the latest vulnerable scan as remediated in the database
    latest_scan = db.query(models.SecurityScanLog).filter(models.SecurityScanLog.status == "vulnerable").order_by(models.SecurityScanLog.timestamp.desc()).first()
    if latest_scan:
        latest_scan.remediated = True
        db.commit()
    
    return {
        "message": "Remediation triggered successfully.",
        "script_path": script_path,
        "alerts_fixed": alerts
    }


@app.get("/api/v1/history")
async def get_scan_history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logs = db.query(models.SecurityScanLog).order_by(models.SecurityScanLog.timestamp.desc()).offset(skip).limit(limit).all()
    return {"history": logs}

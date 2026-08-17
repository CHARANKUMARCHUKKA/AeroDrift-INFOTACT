from fastapi import FastAPI
from enterprise_logger import setup_enterprise_logger

logger = setup_enterprise_logger("AeroDrift.API")
app = FastAPI(title="AeroDrift Enterprise API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    logger.info("AeroDrift API Server Booting Up...")

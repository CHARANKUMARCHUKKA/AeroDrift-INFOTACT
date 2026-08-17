![CI/CD Pipeline](https://github.com/CHARANKUMARCHUKKA/AeroDrift-INFOTACT/actions/workflows/python-app.yml/badge.svg)\n\n# AeroDrift: Agentic Cloud Topology & Remediation Graph

This is the repository for the AeroDrift project, built during the Infotact Solutions Internship (Month 1).

## Team Members
- Charan Kumar Chukka
- Pudi Gowtham Kumar (Team Lead)

## Project Overview
AeroDrift is an autonomous "self-healing" infrastructure engine designed to intercept cloud configuration drift, model it as a directed graph, and programmatically generate remediation scripts.

### Tech Stack
- **Cloud Ingestion:** `boto3`, `asyncio`
- **Topology Engine:** `NetworkX`
- **Code Generator:** Python `ast`
- **Dashboard:** `Rich` (CLI)

## Week-wise Plan
- **Week 1:** AWS Ingestion & Graph Foundations
- **Week 2:** Drift Detection & CLI Interface
- **Week 3:** Agentic Remediation & Execution Sandbox
- **Week 4:** State Persistence & Final Polish

## Setup Instructions
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`

## Daily Work Log
- **Day 1:** Initialized Git repository, setup `README.md`, `requirements.txt`, and `.gitignore`. Built the core `aws_ingestion.py` and `graph_engine.py` for AeroDrift Week 1.
- **Day 2:** Refactored the core ingestion engine to use `asyncio` for high-concurrency polling and added network resiliency/retry logic. Built the NetworkX Cloud Topology Engine and the `Rich` CLI dashboard.
- **Day 3:** Built the `DriftDetector` module to programmatically scan the graph for cybersecurity anti-patterns (e.g., exposed public subnets, overly permissive 0.0.0.0/0 Security Groups). Implemented the Pytest framework with 8 automated tests.
- **Day 4:** Developed the **Auto-Remediation Engine** (`remediation_engine.py`) to parse Drift Detector alerts and automatically generate an AWS CLI bash script (`remediate_drift.sh`) to patch cloud vulnerabilities.
- **Day 5:** Configured an Enterprise CI/CD Pipeline using GitHub Actions (`python-app.yml`). Implemented automated matrix testing (Python 3.10-3.12) and strict code-quality linting using `flake8`.
- **Day 6:** Containerized the AeroDrift engine by creating a highly-optimized, secure `Dockerfile` running on a non-root user. Orchestrated local deployments with `docker-compose.yml`.
- **Day 7:** Built an **Advanced Enterprise JSON Logging System** (`enterprise_logger.py`). Configured file rotation handlers and integrated structured JSON logging across all 4 core engines for Splunk/Datadog compatibility.

## Auto-Remediation Engine
AeroDrift includes an advanced `AutoRemediator` class. When the Drift Detector flags vulnerabilities (like exposed subnets or overly permissive security groups), the Auto-Remediator parses those alerts and automatically generates an AWS CLI bash script (`remediate_drift.sh`) to patch the vulnerabilities without human intervention.

## 🐳 Docker Deployment

AeroDrift is fully containerized for enterprise deployments.

**Build the image:**
```bash
docker build -t aerodrift .
```

**Run the engine:**
```bash
docker run --rm aerodrift
```

**Using Docker Compose:**
```bash
docker-compose up --build
```

## 📊 Enterprise Logging
AeroDrift features an enterprise-grade JSON logging system. All operations are automatically logged in structured JSON format to `logs/aerodrift.json` with a 5MB automatic rotation policy, making it instantly compatible with Splunk, Datadog, and ELK stacks.

## ☁️ Live AWS Boto3 Integration
AeroDrift supports both `MOCK` mode for testing and `LIVE` mode for connecting to real AWS accounts.

**To run in LIVE mode:**
1. Export your AWS Credentials:
   ```bash
   export AWS_ACCESS_KEY_ID="your_key"
   export AWS_SECRET_ACCESS_KEY="your_secret"
   ```
2. Set the engine mode:
   ```bash
   export AERODRIFT_MODE="LIVE"
   ```
3. Required IAM Permissions:
   - `ec2:DescribeInstances`
   - `ec2:DescribeSubnets`
   - `ec2:DescribeSecurityGroups`

## 🌐 REST API (FastAPI)
AeroDrift is accessible via a high-performance REST API.
Start the server locally:
```bash
uvicorn api:app --reload
```
- **Swagger Docs:** `http://localhost:8000/docs`
- **Health Check:** `curl http://localhost:8000/health`
- **Get Topology:** `curl http://localhost:8000/api/v1/topology`
- **Scan Drift:** `curl http://localhost:8000/api/v1/drift`
- **Auto-Remediate:** `curl -X POST http://localhost:8000/api/v1/remediate`

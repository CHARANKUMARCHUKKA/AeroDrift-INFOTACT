![CI/CD Pipeline](https://github.com/CHARANKUMARCHUKKA/AeroDrift-INFOTACT/actions/workflows/python-app.yml/badge.svg)\n\n# AeroDrift: Agentic Cloud Topology & Remediation Graph

This is the repository for the AeroDrift project, built during the Infotact Solutions Internship (Month 1).

## Team Members
- Charan Kumar Chukka (Team Lead)
- Pudi Gowtham Kumar

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

## Daily Work Log (Charan Kumar Chukka)
- **Day 1:** Initialized Git repository, setup `README.md`, `requirements.txt`, and `.gitignore`. Built the core `aws_ingestion.py` and `graph_engine.py` for AeroDrift Week 1.

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

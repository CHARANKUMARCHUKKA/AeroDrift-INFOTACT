# 🛡️ AeroDrift: Multi-Cloud Drift Detection Engine

**AeroDrift** is an automated, enterprise-grade infrastructure drift detection and DevSecOps remediation platform. Designed to solve the challenge of "shadow IT" and unapproved manual changes, AeroDrift actively monitors cloud architectures across **AWS, Azure, and GCP** to identify exposed subnets, unauthorized firewall rules, and critical security vulnerabilities.

---

## 🚀 Key Features

- **Multi-Cloud Topology Mapping:** Ingests state from AWS, Azure, and GCP and models it using a mathematical `NetworkX` graph to identify cross-resource vulnerabilities.
- **Asynchronous Security Scanning:** Utilizes FastAPI `BackgroundTasks` to execute massive compliance scans without blocking the user interface.
- **Automated Remediation Engine:** Capable of automatically reverting dangerous infrastructure changes (e.g., closing exposed ports).
- **Enterprise Dashboard:** An interactive `Streamlit` web portal featuring JWT Authentication, Role-Based Access Control (RBAC), and Plotly data visualizations.
- **SOC2 Compliance Reporting:** One-click CSV export of historical audit logs for compliance officers.
- **Real-Time Alerting:** Integrated SMTP Email digests and Webhooks for Slack and Microsoft Teams.
- **Custom Rules Engine:** Define your own security signatures and forbidden ports via `custom_rules.json`.

---

## 🛠️ Tech Stack

- **Backend:** Python 3, FastAPI, Uvicorn, NetworkX, SQLite, SQLAlchemy, Passlib (bcrypt)
- **Frontend:** Streamlit, Plotly, Pandas
- **DevSecOps:** GitHub Actions, Bandit (SAST), Safety (Dependency Scanning)
- **Infrastructure:** Docker, Docker Compose, Kubernetes, Terraform

---

## 💻 How to Run Locally

### 1. Install Dependencies
Ensure you have Python installed, activate your virtual environment, and run:
```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI Backend
Start the core asynchronous engine on port 8000:
```bash
python -m uvicorn api:app --reload
```

### 3. Start the Streamlit Dashboard
Open a **new terminal window**, activate your virtual environment, and run the UI on port 8501:
```bash
python -m streamlit run dashboard.py
```

### 4. Login
Open your browser to `http://localhost:8501`.
- **Username:** `admin`
- **Password:** `aerodrift2026`

---

## 🏗️ Deployment (Production)

AeroDrift is built for enterprise deployment. The repository includes:
- **Docker Compose:** `docker-compose up --build -d`
- **Kubernetes:** Apply the manifests located in the `/k8s` directory (`kubectl apply -f k8s/`).
- **Terraform:** Provision AWS EC2 infrastructure using the modules in the `/terraform` directory.

---

## 📜 Architecture Overview
For a deep dive into the system components, data flow, and threat models, please refer to the [ARCHITECTURE.md](ARCHITECTURE.md) document.

---
*Developed as the Final Project for the Infotact Solutions Software Engineering Internship.*
*Release: v1.0.0*

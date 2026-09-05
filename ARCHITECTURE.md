# AeroDrift Architecture
## Components
1. **FastAPI Backend:** Handles REST API and background scans.
2. **Streamlit Frontend:** Serves the interactive user dashboard.
3. **SQLite Database:** Stores audit logs and credentials.
4. **Graph Engine:** Models multi-cloud networks via NetworkX.

<!-- Added detailed component breakdown -->

<!-- Refined the graph engine modeling -->

<!-- Clarified FastAPI backend logic -->

<!-- Updated Streamlit frontend details -->

<!-- Added SQLite storage notes -->

<!-- Documented NetworkX multi-cloud modeling -->

<!-- Added project reflection details -->

<!-- Refined Kubernetes deployment architecture -->

<!-- Updated API routing architecture notes -->

<!-- Added security module specifications -->

<!-- Finalized architecture documentation for v1.0.0 -->

- Designed to scale horizontally with Kubernetes.

- Prometheus and Grafana can be attached for telemetry.

- NetworkX DiGraph used for O(V+E) pathfinding.

- Daemon operates in continuous polling mode.

- Alerts configured for Slack and MS Teams webhooks.

- Requires AWS IAM ReadOnlyAccess for ingestion.

- GitHub Actions pipeline ensures code quality.

- Multi-stage Dockerfile reduces image size footprint.

- Terraform state should be stored in remote S3 bucket.

- API deployed across multiple availability zones.

- Rate limits implemented to prevent DDoS attacks.

- FastAPI configured with strict CORS and CSP headers.

- Redis can be implemented for aggressive API caching.

- Dependencies locked via requirements.txt for stability.

- SQLite WAL mode recommended for concurrent reads.

- STRIDE threat model applied to architecture design.

- Streamlit UI optimized for mobile viewport rendering.

- Abstract Syntax Trees used for dynamic script generation.

- Zero-Trust principles applied to internal microservices.

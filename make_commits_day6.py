import os
import subprocess
import time

def commit_files(filepaths_content_map, message):
    for fp, content in filepaths_content_map.items():
        os.makedirs(os.path.dirname(fp) or '.', exist_ok=True)
        with open(fp, 'w') as f:
            f.write(content)
        subprocess.run(["git", "add", fp], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)
    time.sleep(1)  # small sleep to ensure commit timestamps are distinct

# 1. build: add .dockerignore to exclude virtual environments and cache
dockerignore_content = """venv/
__pycache__/
*.pyc
.pytest_cache/
.github/
.git/
"""
commit_files({".dockerignore": dockerignore_content}, "build: add .dockerignore to exclude virtual environments and cache")

# 2. build: create base Dockerfile with Python 3.12 slim image
dockerfile_content = """# AeroDrift Enterprise Dockerfile
FROM python:3.12-slim
"""
commit_files({"Dockerfile": dockerfile_content}, "build: create base Dockerfile with Python 3.12 slim image")

# 3. build: configure Docker working directory and system dependencies
dockerfile_content += """
WORKDIR /app

# Install system dependencies required for underlying libraries
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*
"""
commit_files({"Dockerfile": dockerfile_content}, "build: configure Docker working directory and system dependencies")

# 4. build: add dependency installation step to Dockerfile
dockerfile_content += """
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
"""
commit_files({"Dockerfile": dockerfile_content}, "build: add dependency installation step to Dockerfile")

# 5. build: copy AeroDrift source code into Docker container
dockerfile_content += """
COPY . .
"""
commit_files({"Dockerfile": dockerfile_content}, "build: copy AeroDrift source code into Docker container")

# 6. build: add non-root user for Docker container security
dockerfile_content += """
# Security: Run as non-root user
RUN useradd -m aerodrift
USER aerodrift
"""
commit_files({"Dockerfile": dockerfile_content}, "build: add non-root user for Docker container security")

# 7. build: configure Docker entrypoint for graph_engine.py
dockerfile_content += """
# Default entrypoint starts the Cloud Topology Engine
CMD ["python", "graph_engine.py"]
"""
commit_files({"Dockerfile": dockerfile_content}, "build: configure Docker entrypoint for graph_engine.py")

# 8. test: add docker-compose.yml for local testing orchestration
docker_compose_content = """version: '3.8'

services:
  aerodrift-engine:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: aerodrift-engine
    restart: "no"
"""
commit_files({"docker-compose.yml": docker_compose_content}, "test: add docker-compose.yml for local testing orchestration")

# 9. ci: add Docker build verification to GitHub Actions pipeline
with open(".github/workflows/python-app.yml", "r") as f:
    ci_content = f.read()

ci_content += """
  docker-build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Build Docker image
      run: docker build . --file Dockerfile --tag aerodrift:latest
"""
commit_files({".github/workflows/python-app.yml": ci_content}, "ci: add Docker build verification to GitHub Actions pipeline")

# 10. docs: update README with Docker build and run instructions
with open("README.md", "r") as f:
    readme_content = f.read()

docker_readme = """
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
"""
readme_content += docker_readme
commit_files({"README.md": readme_content}, "docs: update README with Docker build and run instructions")

os.remove(__file__)

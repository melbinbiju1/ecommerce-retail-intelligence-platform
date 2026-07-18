# Docker Setup

## Purpose

This document explains how to build and run the FastAPI backend for the **E-Commerce Retail Intelligence Platform** inside a Docker container.

Docker is used in this project to package the API and its Python dependencies into a reproducible runtime environment.

This helps demonstrate:

- Application containerisation
- Reproducible local execution
- API deployment readiness
- Cloud deployment preparation
- Separation between local development and container-based execution

## What Docker Runs in This Project

The Docker container runs the FastAPI backend.

The API serves:

- Executive KPI endpoints
- Sales performance endpoints
- Operational anomaly endpoints
- Operational risk endpoints
- AI-ready business insight endpoints
- Health check endpoints

The local Docker version uses the SQLite database file:

```text
retail_intelligence.db
```

The database file is **not copied into the Docker image**.

Instead, it is mounted into the container at runtime using a Docker volume mount.

This keeps the Docker image smaller and separates the application image from local runtime data.

In the Azure version of the project, the API will connect to Azure SQL Database instead of using the local SQLite file.

## Docker Files

| File | Purpose |
|---|---|
| `Dockerfile` | Defines how the FastAPI API container image is built |
| `.dockerignore` | Excludes unnecessary local files from the Docker build context |
| `docker/README.md` | Documents Docker build, run, stop, volume mount, and troubleshooting commands |

## Dockerfile Summary

The Dockerfile performs the following steps:

1. Uses a lightweight Python image.
2. Sets `/app` as the working directory.
3. Copies `requirements.txt`.
4. Installs Python dependencies.
5. Copies the API source code.
6. Copies project data and logging folders needed by the app.
7. Exposes port `8000`.
8. Starts the FastAPI app using Uvicorn.

The Dockerfile does **not** copy the SQLite database into the image.

The API is started with:

```text
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

## Build Docker Image

Run this command from the project root:

```powershell
docker build -t ecommerce-retail-api .
```

This creates a Docker image named:

```text
ecommerce-retail-api
```

## Run Docker Container with SQLite Volume Mount

Run this command from the project root:

```powershell
docker run --name ecommerce-retail-api-container -p 8000:8000 -v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db ecommerce-retail-api
```

This starts the API container and mounts the local SQLite database into the container.

| Part | Meaning |
|---|---|
| `-p 8000:8000` | Maps local port `8000` to container port `8000` |
| `-v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db` | Mounts the local SQLite database into the container |
| `ecommerce-retail-api` | Docker image name |

After starting the container, open:

```text
http://127.0.0.1:8000/docs
```

This opens the FastAPI Swagger documentation page.

## Run Docker Container in Detached Mode

Detached mode runs the container in the background.

```powershell
docker run -d --name ecommerce-retail-api-container -p 8000:8000 -v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db ecommerce-retail-api
```

Check running containers:

```powershell
docker ps
```

View container logs:

```powershell
docker logs ecommerce-retail-api-container
```

Stop the container:

```powershell
docker stop ecommerce-retail-api-container
```

Remove the container:

```powershell
docker rm ecommerce-retail-api-container
```

## If the Container Name Already Exists

If you see an error like:

```text
The container name "/ecommerce-retail-api-container" is already in use
```

stop and remove the old container:

```powershell
docker stop ecommerce-retail-api-container
docker rm ecommerce-retail-api-container
```

Then run the container again:

```powershell
docker run --name ecommerce-retail-api-container -p 8000:8000 -v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db ecommerce-retail-api
```

## API URL

When the container is running, the API is available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health/
```

System status endpoint:

```text
http://127.0.0.1:8000/health/status
```

## API Authentication

Protected endpoints require the `X-API-Key` header.

Demo API keys are used for local testing.

| Role | Demo Key |
|---|---|
| Admin | `admin-demo-key` |
| Analyst | `analyst-demo-key` |
| Viewer | `viewer-demo-key` |

In Swagger UI:

1. Open `http://127.0.0.1:8000/docs`
2. Click **Authorize**
3. Enter one of the demo API keys
4. Test protected endpoints

## Recommended Endpoints to Test

Public endpoints:

```text
/
```

```text
/health/
```

```text
/health/status
```

Protected executive endpoint:

```text
/executive/summary
```

Protected operations endpoint:

```text
/operations/alert-summary
```

Protected AI-ready insight endpoint:

```text
/insights/executive-summary
```

Admin-only LLM context endpoint:

```text
/insights/llm-context
```

## Docker Ignore Rules

The `.dockerignore` file excludes unnecessary files from the Docker image build process.

Examples of files and folders ignored:

```text
.venv
venv
__pycache__
*.pyc
.pytest_cache
.git
dbt_retail/target
dbt_retail/logs
dbt_retail/.dbt
notebooks
*.pbix
.env
*.log
retail_intelligence.db
*.db
*.sqlite
*.sqlite3
```

The SQLite database is ignored in `.dockerignore` because it is mounted into the container at runtime instead of being copied into the Docker image.

## Difference Between `.dockerignore` and `.gitignore`

| File | Purpose |
|---|---|
| `.dockerignore` | Controls what is excluded from the Docker build context |
| `.gitignore` | Controls what is excluded from GitHub |

For this project:

| Item | `.dockerignore` | `.gitignore` | Reason |
|---|---|---|---|
| `dbt_retail/.dbt` | Ignore | Ignore | Local dbt configuration/cache |
| `dbt_retail/target` | Ignore | Ignore | Generated dbt artifacts |
| `dbt_retail/logs` | Ignore | Ignore | Generated dbt logs |
| `retail_intelligence.db` | Ignore | Ignore | Large generated local database; mounted at runtime for Docker |

## Docker Desktop Version Notes

Docker may show different version numbers for Docker Desktop and Docker Engine.

Example:

```text
Docker Desktop 4.82.0
Docker Engine 29.6.1
```

This is normal.

| Component | Meaning |
|---|---|
| Docker Desktop | The Windows desktop application that manages Docker |
| Docker Engine | The backend service that builds and runs containers |
| Docker CLI | The command-line tool used from PowerShell |

A working setup should show both `Client` and `Server` sections when running:

```powershell
docker version
```

## Useful Docker Commands

Check Docker version:

```powershell
docker version
```

Check Docker system information:

```powershell
docker info
```

List running containers:

```powershell
docker ps
```

List all containers:

```powershell
docker ps -a
```

List Docker images:

```powershell
docker images
```

Build image:

```powershell
docker build -t ecommerce-retail-api .
```

Run container with SQLite mount:

```powershell
docker run --name ecommerce-retail-api-container -p 8000:8000 -v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db ecommerce-retail-api
```

Run container in background with SQLite mount:

```powershell
docker run -d --name ecommerce-retail-api-container -p 8000:8000 -v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db ecommerce-retail-api
```

View logs:

```powershell
docker logs ecommerce-retail-api-container
```

Stop container:

```powershell
docker stop ecommerce-retail-api-container
```

Remove container:

```powershell
docker rm ecommerce-retail-api-container
```

Remove image:

```powershell
docker rmi ecommerce-retail-api
```

## Troubleshooting

### Docker daemon is not running

If you see:

```text
docker daemon is not running
```

open Docker Desktop and wait until the engine is running.

Then run:

```powershell
docker version
```

The output should show both:

```text
Client
Server
```

### Docker command hangs

If `docker info` or `docker version` hangs, try:

```powershell
wsl --shutdown
```

Then restart Docker Desktop.

### Container name already exists

Stop and remove the existing container:

```powershell
docker stop ecommerce-retail-api-container
docker rm ecommerce-retail-api-container
```

Then run the container again.

### Port 8000 already in use

If port `8000` is already being used, run the container on another local port:

```powershell
docker run --name ecommerce-retail-api-container -p 8001:8000 -v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db ecommerce-retail-api
```

Then open:

```text
http://127.0.0.1:8001/docs
```

### API starts but database endpoints fail

Make sure the SQLite database is mounted correctly.

Run the container from the project root and include:

```powershell
-v ${PWD}\retail_intelligence.db:/app/retail_intelligence.db
```

The local file must exist:

```powershell
Get-Item retail_intelligence.db
```

### API starts but protected endpoints fail

Make sure you are passing an API key using the `X-API-Key` header.

In Swagger UI, click **Authorize** and enter:

```text
admin-demo-key
```

## Local vs Cloud Version

The local Docker version is designed for portfolio demonstration and local testing.

| Local Docker Version | Future Azure Version |
|---|---|
| Mounts SQLite database at runtime | Uses Azure SQL Database |
| Uses demo API keys from environment settings | Uses secure secrets from Azure Key Vault |
| Runs locally on Docker Desktop | Runs on Azure App Service or container hosting |
| Used for development and demonstration | Used for cloud deployment |

## Interview Explanation

A simple interview explanation for this phase:

```text
I containerised the FastAPI backend using Docker so the API can run in a reproducible environment. To keep the image lightweight and closer to production practice, I do not copy the local SQLite database into the image. Instead, I mount the SQLite database at runtime for local demonstration. In the cloud version, the same API structure can connect to Azure SQL Database, with secrets managed through Azure Key Vault. This prepares the project for CI/CD and cloud deployment.
```

## Phase Outcome

This Docker phase proves that the API can be packaged and executed consistently outside the local Python virtual environment.

It demonstrates deployment readiness for the backend layer of the project while keeping application code and runtime data separated.
# Azure App Deployment

## Purpose

This phase deploys the FastAPI backend for the E-Commerce Retail Intelligence Platform to Azure App Service as a Docker container.

Before this phase, the API could be tested locally using either SQLite or Azure SQL Database. After this phase, the API is available as a cloud-hosted service and can serve business KPIs, operational risk metrics, anomaly alerts, and AI-ready insight endpoints through HTTPS.

The deployed API connects to Azure SQL Database, not the local SQLite database.

---

## Deployment Summary

| Area | Implementation |
|---|---|
| Application framework | FastAPI |
| Container runtime | Docker |
| Container registry | Azure Container Registry |
| Cloud hosting | Azure App Service for Containers |
| Database backend | Azure SQL Database |
| Authentication | API key based RBAC |
| Runtime mode | `APP_ENV=azure` |
| Public access | HTTPS Azure App Service URL |

---

## Deployment Architecture

```text
Local project source code
        ↓
Docker image build
        ↓
Azure Container Registry
        ↓
Azure App Service for Containers
        ↓
FastAPI cloud API
        ↓
Azure SQL Database
```

The deployment separates the application layer from the data layer:

- The Docker image contains the FastAPI application code and Python dependencies.
- The Docker image does not contain the local SQLite database.
- Azure SQL Database stores the curated warehouse tables and API serving objects.
- Azure App Service runs the container and exposes the API over HTTPS.
- App Service environment variables control database connection settings and API keys.

---

## Azure Resources

| Resource Type | Resource Name |
|---|---|
| Resource Group | `rg-ecommerce-retail-intelligence` |
| Azure Container Registry | `acrecommerceretailmelbin` |
| Container Image | `ecommerce-retail-api:latest` |
| Azure App Service | `app-ecommerce-retail-api-melbin` |
| App Service Region | `France Central` |
| Azure SQL Database | `sqldb-ecommerce-retail-intelligence` |

The deployed application default domain is:

```text
https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net
```

---

## Container Image

The FastAPI application is packaged as a Docker image.

The image includes:

- Python runtime
- FastAPI application code
- API routes
- Authentication logic
- Azure SQL connectivity code
- ODBC dependencies required for SQL Server
- Python package dependencies from `requirements.txt`

The image excludes:

- Local SQLite database files
- `.env` secrets
- Virtual environments
- Cache folders
- Power BI files
- Local notebook artifacts

This keeps the image smaller, safer, and suitable for cloud deployment.

---

## Dockerfile Notes

The deployment Dockerfile uses a Debian Bookworm-based Python image so that the Microsoft ODBC Driver 18 for SQL Server can be installed reliably.

The API runs with:

```text
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

Azure App Service is configured with:

```text
WEBSITES_PORT=8000
```

This tells Azure which port the containerized API is listening on.

---

## Azure Container Registry

Azure Container Registry stores the built Docker image.

The image was tagged using the ACR login server:

```text
acrecommerceretailmelbin.azurecr.io/ecommerce-retail-api:latest
```

Example image push workflow:

```powershell
docker build -t ecommerce-retail-api .

docker tag ecommerce-retail-api acrecommerceretailmelbin.azurecr.io/ecommerce-retail-api:latest

docker push acrecommerceretailmelbin.azurecr.io/ecommerce-retail-api:latest
```

---

## App Service Container Configuration

The Azure App Service is configured as a Linux container application.

| Setting | Value |
|---|---|
| Publish mode | Container |
| Operating system | Linux |
| Image source | Azure Container Registry |
| Registry | `acrecommerceretailmelbin` |
| Image | `ecommerce-retail-api` |
| Tag | `latest` |
| Port | `8000` |
| Startup command | Blank |

The startup command is left blank because the Dockerfile already defines the container startup command.

---

## Managed Identity for ACR Pull

The App Service uses managed identity to access Azure Container Registry.

This avoids enabling ACR admin credentials and avoids storing registry passwords inside App Service.

The Web App system-assigned managed identity is granted the following role on the Azure Container Registry:

```text
AcrPull
```

This permission allows the App Service to pull the container image securely from ACR.

---

## Runtime Environment Variables

The deployed API is configured through Azure App Service environment variables.

These are added in:

```text
Azure Portal
→ App Services
→ app-ecommerce-retail-api-melbin
→ Settings
→ Environment variables
→ App settings
```

Required settings:

| Variable | Purpose |
|---|---|
| `APP_ENV` | Selects local SQLite mode or Azure SQL mode |
| `AZURE_SQL_SERVER` | Azure SQL Server hostname |
| `AZURE_SQL_DATABASE` | Azure SQL Database name |
| `AZURE_SQL_USERNAME` | Azure SQL login username |
| `AZURE_SQL_PASSWORD` | Azure SQL login password |
| `AZURE_SQL_DRIVER` | ODBC driver used by SQLAlchemy and pyodbc |
| `ADMIN_API_KEY` | Admin API key for protected API endpoints |
| `ANALYST_API_KEY` | Analyst API key for protected API endpoints |
| `VIEWER_API_KEY` | Viewer API key for protected API endpoints |
| `WEBSITES_PORT` | Container port used by Azure App Service |

The deployed value for runtime mode is:

```text
APP_ENV=azure
```

This makes the API connect to Azure SQL Database instead of SQLite.

---

## Database Connection Mode

The API supports two database modes.

| Mode | Setting | Database |
|---|---|---|
| Local development | `APP_ENV=local` | SQLite |
| Cloud deployment | `APP_ENV=azure` | Azure SQL Database |

This design allows the same API codebase to run locally and in Azure.

In local mode, the API reads from:

```text
retail_intelligence.db
```

In Azure mode, the API reads from:

```text
sqldb-ecommerce-retail-intelligence
```

---

## API Serving Objects in Azure SQL

The FastAPI endpoints depend on serving-layer objects such as:

- `vw_executive_summary`
- `vw_monthly_sales`
- `vw_product_performance`
- `vw_seller_performance`
- `vw_customer_state_performance`
- `vw_operational_alert_summary`
- `vw_operational_alerts_by_type`
- `vw_operational_alerts_by_severity`
- `vw_recent_operational_alerts`
- `vw_high_risk_sellers`
- `vw_high_risk_categories`
- `vw_operational_risk_summary`

For Azure SQL deployment, these API serving objects are migrated from local SQLite views into Azure SQL tables with the same names.

Migration script:

```powershell
python scripts\migrate_api_serving_views_to_azure_sql.py
```

Migration report:

```text
data/processed/azure_sql_api_serving_views_migration_report.csv
```

This ensures the deployed API can serve the same routes as the local API.

---

## Public API Endpoints

These endpoints are available without an API key:

| Endpoint | Purpose |
|---|---|
| `/` | API landing response |
| `/health/` | API and database health check |
| `/docs` | Swagger API documentation |
| `/openapi.json` | OpenAPI schema |

Example:

```text
https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net/health/
```

---

## Protected API Endpoints

Protected endpoints require an API key in the request header:

```text
X-API-Key: admin-demo-key
```

Example PowerShell request:

```powershell
$headers = @{
    "X-API-Key" = "admin-demo-key"
}

Invoke-RestMethod `
  -Uri "https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net/executive/summary" `
  -Headers $headers
```

Example protected endpoints:

| Endpoint | Purpose |
|---|---|
| `/executive/summary` | Executive KPI summary |
| `/executive/monthly-sales` | Monthly sales trends |
| `/executive/top-products` | Top product categories |
| `/executive/top-sellers` | Seller performance |
| `/operations/alert-summary` | Operational alert summary |
| `/operations/recent-alerts` | Recent anomaly alerts |
| `/operations/high-risk-sellers` | High-risk seller list |
| `/operations/high-risk-categories` | High-risk category list |
| `/insights/executive-summary` | AI-ready executive insight summary |
| `/insights/recommendations` | Business recommendation insights |

---

## Deployment Verification

Deployment is verified using:

```powershell
python scripts\verify_azure_app_deployment.py
```

The script checks:

- Root endpoint
- Health endpoint
- Executive summary endpoint
- Operational alert summary endpoint
- AI-ready executive insight endpoint

Verification output:

```text
data/processed/azure_app_deployment_verification_report.csv
```

A successful deployment returns HTTP 200 for all tested endpoints.

---

## Health Check

The health endpoint confirms both the API and database connection.

Expected response:

```json
{
  "status": "ok",
  "service": "E-Commerce Retail Intelligence API",
  "database_connected": true
}
```

If `database_connected` is `false`, common causes include:

- Missing App Service environment variables
- Incorrect Azure SQL password
- Azure SQL firewall restrictions
- Azure SQL database paused or unavailable
- Incorrect ODBC driver setting
- Incorrect `APP_ENV` value

---

## Security Notes

Current security controls:

- `.env` file is not committed to GitHub.
- Runtime secrets are stored as App Service environment variables.
- API endpoints are protected using API keys.
- Role-based API access is implemented for Admin, Analyst, and Viewer users.
- ACR image pull uses managed identity with `AcrPull` role.

Current limitations:

- API keys are still stored directly as App Service environment variables.
- SQL username/password are still stored as App Service environment variables.
- Key Vault integration is not yet implemented.

The next security improvement is Azure Key Vault integration.

---

## Cost Control Notes

The App Service was deployed using a low-cost/free tier where available.

For portfolio demonstration, this is sufficient because:

- The API workload is lightweight.
- Heavy data storage is handled by Azure SQL Database.
- The app is used for demonstration and testing, not production traffic.

Recommended cost-control actions:

- Stop the App Service when not testing.
- Keep Azure SQL auto-pause enabled if using serverless/free configuration.
- Monitor Azure resource costs regularly.
- Avoid scaling the App Service plan unless needed.

---

## Troubleshooting

### Container does not start

Check:

```text
App Service → Log stream
```

Common causes:

- Container image not selected correctly
- Wrong image tag
- Missing `WEBSITES_PORT=8000`
- Startup failure inside FastAPI
- Missing ODBC driver in Dockerfile

---

### App Service cannot pull image from ACR

Check:

```text
App Service → Identity
Container Registry → Access control (IAM)
```

The Web App managed identity must have:

```text
AcrPull
```

on the Azure Container Registry.

---

### Health endpoint works but protected endpoints fail

Check:

- API key header is included.
- Correct header name is used: `X-API-Key`.
- The correct role key is used.
- App Service environment variables contain the API keys.

---

### Protected endpoints return database object errors

Check that the API serving objects were migrated to Azure SQL:

```powershell
python scripts\migrate_api_serving_views_to_azure_sql.py
```

Then restart the Web App.

---

## Interview Explanation

A concise explanation for interviews:

```text
I containerized the FastAPI backend with Docker and deployed it to Azure App Service for Containers. The image is stored in Azure Container Registry, and the App Service pulls the image using managed identity with AcrPull permissions. The deployed API runs in Azure SQL mode using App Service environment variables, so the cloud API connects to Azure SQL Database instead of the local SQLite database. I verified the deployment using health checks and authenticated business endpoints.
```

A more technical explanation:

```text
The deployment follows a container-based architecture. I build the FastAPI application into a Docker image, push it to Azure Container Registry, and host it on Azure App Service as a Linux container. Runtime configuration is injected through App Service environment variables, including APP_ENV=azure, SQL Server connection settings, and API keys. The API uses SQLAlchemy and pyodbc with Microsoft ODBC Driver 18 to connect to Azure SQL Database. The Web App uses a system-assigned managed identity with AcrPull permission to securely pull the image from ACR.
```

---

## Phase Outcome

At the end of this phase, the project has a deployed cloud API.

The platform now includes:

```text
Azure Blob Storage
        ↓
Azure Data Factory
        ↓
Azure SQL Database
        ↓
Azure App Service FastAPI backend
        ↓
Authenticated business and operational API endpoints
```

This completes the cloud application deployment layer of the project.
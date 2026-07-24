# GitHub Actions CI/CD for Azure App Service

## Purpose

This phase adds a professional continuous deployment workflow to the project.

Before this phase, the project had GitHub Actions CI and a manual Azure deployment process.

The deployment flow was:

```text
Manual Docker build
    ↓
Manual Docker push to Azure Container Registry
    ↓
Azure App Service runs the container image
```

After this phase, the project has CI/CD:

```text
Push to main branch
    ↓
GitHub Actions CI validation
    ↓
GitHub Actions CD deployment
    ↓
Docker image build
    ↓
Push image to Azure Container Registry
    ↓
Update Azure App Service container image
    ↓
Restart Azure App Service
    ↓
Verify deployed /health/ endpoint
```

This makes the deployment process more professional, repeatable, and closer to a real cloud engineering workflow.

---

## CI/CD Architecture

```text
Developer pushes code to GitHub main branch
        ↓
GitHub Actions CI Pipeline
        ↓
Validate code, imports, Docker setup, and Docker image build
        ↓
GitHub Actions CD Pipeline
        ↓
Login to Azure using service principal
        ↓
Build Docker image
        ↓
Push Docker image to Azure Container Registry
        ↓
Ensure App Service managed identity and AcrPull permission
        ↓
Configure App Service to use managed identity for ACR
        ↓
Set App Service container image
        ↓
Restart Azure App Service
        ↓
Verify deployed /health/ endpoint
```

---

## GitHub Actions Workflows

The project has two GitHub Actions workflows.

| Workflow | File | Purpose |
|---|---|---|
| CI Pipeline | `.github/workflows/ci.yml` | Validates the project on every push |
| CD Pipeline | `.github/workflows/cd-azure-app.yml` | Builds, pushes, deploys, and verifies the API container |

---

## CI Pipeline

The CI workflow validates the repository before deployment.

The CI pipeline checks:

- Large local SQLite database is not tracked by Git
- Python dependencies install successfully
- Python source files compile
- Core imports work
- Docker setup verification passes
- CI setup verification passes
- Docker image builds successfully

CI workflow file:

```text
.github/workflows/ci.yml
```

CI screenshot:

```text
docs/images/02a_ci_pipeline_success.png
```

Markdown reference:

```markdown
![GitHub Actions CI Pipeline success](images/02a_ci_pipeline_success.png)
```

---

## CD Pipeline

The CD workflow deploys the FastAPI container to Azure App Service.

CD workflow file:

```text
.github/workflows/cd-azure-app.yml
```

The CD workflow performs these steps:

1. Checks out the repository
2. Logs in to Azure
3. Logs in to Azure Container Registry
4. Builds the Docker image
5. Tags the image as both `latest` and the Git commit SHA
6. Pushes the image to Azure Container Registry
7. Ensures App Service managed identity exists
8. Ensures the App Service identity has `AcrPull` permission
9. Configures App Service to use managed identity for ACR image pull
10. Sets the App Service container image
11. Restarts Azure App Service
12. Waits for application startup
13. Verifies the deployed `/health/` endpoint with retries

CD screenshot:

```text
docs/images/02b_cd_pipeline_success.png
```

Markdown reference:

```markdown
![GitHub Actions CD Pipeline success](images/02b_cd_pipeline_success.png)
```

---

## Azure Resources Used by CD

| Resource | Name |
|---|---|
| Resource group | `rg-ecommerce-retail-intelligence` |
| Azure Container Registry | `acrecommerceretailmelbin` |
| ACR login server | `acrecommerceretailmelbin.azurecr.io` |
| Azure App Service | `app-ecommerce-retail-api-melbin` |
| Container image | `ecommerce-retail-api:latest` |
| Deployed API URL | `https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net` |

---

## GitHub Repository Secrets

The CD workflow uses GitHub repository secrets.

| Secret | Purpose |
|---|---|
| `AZURE_CREDENTIALS` | Azure service principal JSON used by GitHub Actions to log in to Azure |
| `ACR_LOGIN_SERVER` | Azure Container Registry login server |
| `AZURE_WEBAPP_NAME` | Azure App Service name |
| `AZURE_RESOURCE_GROUP` | Azure resource group name |
| `AZURE_APP_BASE_URL` | Base URL of the deployed FastAPI API |

Sensitive values are stored as GitHub Actions secrets and are not committed to the repository.

---

## Azure Authentication Design

GitHub Actions logs in to Azure using a service principal.

The service principal is scoped to the project resource group:

```text
rg-ecommerce-retail-intelligence
```

This allows GitHub Actions to manage the project deployment resources without using a personal account interactively.

---

## Container Deployment Design

The CD workflow builds and pushes two tags for each deployment:

```text
latest
<github-commit-sha>
```

Example image references:

```text
acrecommerceretailmelbin.azurecr.io/ecommerce-retail-api:latest
acrecommerceretailmelbin.azurecr.io/ecommerce-retail-api:<commit-sha>
```

The App Service uses the `latest` tag for deployment.

The commit SHA tag provides traceability between GitHub commits and Docker images.

---

## Managed Identity ACR Pull Design

Azure App Service uses managed identity to pull the Docker image from Azure Container Registry.

This avoids storing ACR username/password credentials in App Service.

The CD workflow explicitly ensures:

```text
App Service managed identity exists
        ↓
App Service identity has AcrPull permission on ACR
        ↓
App Service uses acrUseManagedIdentityCreds=true
        ↓
App Service pulls the container image securely
```

This design fixed the earlier `ImagePullUnauthorizedFailure` issue.

---

## Deployment Verification

The CD workflow verifies deployment using the public health endpoint:

```text
/health/
```

Full URL:

```text
https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net/health/
```

Expected response:

```json
{
  "status": "ok",
  "service": "E-Commerce Retail Intelligence API",
  "database_connected": true
}
```

The workflow uses retry logic because Azure App Service may need time to restart the container after deployment.

---

## Why Only `/health/` Is Checked in CD

The CD workflow performs a deployment smoke test using `/health/`.

This is intentional.

The `/health/` endpoint verifies:

- The deployed FastAPI container is running
- Azure App Service is reachable
- The API can connect to Azure SQL Database
- The deployment did not break application startup

Protected business endpoints are verified separately using local verification scripts:

```text
scripts/verify_azure_app_deployment.py
scripts/verify_key_vault_setup.py
scripts/verify_azure_monitoring_setup.py
```

This avoids storing JWT user credentials or access tokens in GitHub Actions secrets just for deployment smoke testing.

---

## Important Runtime Requirement

The `/health/` endpoint checks Azure SQL connectivity.

Therefore, Azure SQL Database must be online when the CD workflow runs.

If Azure SQL is paused, the CD health check may fail even if the container deployment itself is correct.

---

## Troubleshooting Issue Resolved

During CD setup, the first deployment failed because Azure App Service could not pull the Docker image from Azure Container Registry.

The error was:

```text
ImagePullUnauthorizedFailure
Failed to pull image
Image pull failed with forbidden or unauthorized
```

Root cause:

```text
App Service did not have the correct managed identity based ACR pull configuration.
```

Fix:

```text
Enable App Service managed identity
Assign AcrPull role on ACR
Set acrUseManagedIdentityCreds=true
Reset App Service container image
Restart App Service
Update CD workflow to preserve this configuration
```

This troubleshooting process is now reflected in the final CD workflow.

---

## CI/CD Screenshots

### GitHub Actions CI Pipeline

```markdown
![GitHub Actions CI Pipeline success](images/02a_ci_pipeline_success.png)
```

### GitHub Actions CD Pipeline

```markdown
![GitHub Actions CD Pipeline success](images/02b_cd_pipeline_success.png)
```

---

## Final CI/CD Outcome

The project now has a professional CI/CD workflow:

```text
Code push
    ↓
CI validation
    ↓
Docker build
    ↓
Docker push to ACR
    ↓
Azure App Service deployment
    ↓
Post-deployment health check
```

This allows the project to be described accurately as:

```text
GitHub Actions CI/CD with Docker-based deployment to Azure App Service.
```

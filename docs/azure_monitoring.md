# Azure Monitoring, Logs, and Availability Checks

## Purpose

This phase adds monitoring and availability validation for the deployed FastAPI API.

The goal is to show that the cloud-hosted API is not only deployed, but also observable. Monitoring helps confirm that the API is available, logs are accessible, failures can be investigated, and health checks are tracked over time.

This phase covers:

- Azure App Service logs
- App Service Log Stream
- Application Insights
- Availability testing for the `/health/` endpoint
- Automatic alerting for availability failures
- Monitoring verification report generation

---

## Monitoring Architecture

```text
Azure App Service FastAPI API
        ↓
Application logs and container logs
        ↓
Azure App Service Log Stream

Azure App Service FastAPI API
        ↓
/health/ endpoint
        ↓
Application Insights Availability Test
        ↓
Azure Monitor Alert Rule
```

---

## Azure Resources

| Resource Type | Resource Name |
|---|---|
| Resource Group | `<resource-group-name>` |
| Azure App Service | `<app-service-name>` |
| Application Insights | `<application-insights-name>` |
| Log Analytics Workspace | `<log-analytics-workspace-name>` |
| Availability Test | `fastapi-health-check` |
| Alert Rule | Automatically created availability alert rule |

---

## App Service Logging

Application logging was enabled for the deployed Azure App Service.

Configuration:

| Setting | Value |
|---|---|
| Application logging | File System |
| Log quota | 35 MB |
| Retention period | Short-term retention for portfolio monitoring |
| Log Stream | Enabled through Azure Portal |

Logs can be viewed in:

```text
Azure Portal
→ App Services
→ <app-service-name>
→ Monitoring
→ Log stream
```

The Log Stream was verified by calling the deployed health endpoint:

```text
https://<app-service-hostname>/health/
```

---

## Built-in App Service Health Check

Azure App Service built-in Health Check is not the primary monitoring approach for this project.

During the initial monitoring setup, the API was running on the Free App Service plan, where built-in App Service Health Check was unavailable. The Azure Portal indicated that built-in Health Check requires a Basic B1 or higher App Service plan.

Later, the App Service was upgraded to Basic B1 during CI/CD deployment troubleshooting. However, Application Insights availability testing remains the chosen monitoring approach because it checks the public `/health/` endpoint externally from multiple Azure locations.

This is the chosen monitoring approach for the portfolio version.

---

## Application Insights

Application Insights was created to monitor the deployed API.

| Setting | Value |
|---|---|
| Application Insights resource | `<application-insights-name>` |
| Region | <azure-region> |
| Resource group | `<resource-group-name>` |
| Resource mode | Workspace-based |
| Connected App Service | `<app-service-name>` |

Application Insights provides:

- Availability monitoring
- Basic request observability
- Failure tracking
- Alert integration
- Monitoring evidence for the deployed API

---

## App Service and Application Insights Connection

The deployed App Service was connected to the existing Application Insights resource:

```text
App Services
→ <app-service-name>
→ Settings
→ Application Insights
→ Select existing resource
→ <application-insights-name>
```

Azure added Application Insights-related configuration to the App Service settings.

This allows the deployed App Service to be associated with the Application Insights resource.

---

## Availability Test

A Standard availability test was created for the deployed API health endpoint.

| Field | Value |
|---|---|
| Test name | `fastapi-health-check` |
| Test type | Standard availability test |
| URL | `https://<app-service-hostname>/health/` |
| HTTP method | GET |
| Expected response | HTTP 200 |
| Frequency | 5 minutes |
| Test timeout | 120 seconds |
| Test locations | 5 selected locations |
| SSL certificate validity check | Enabled |
| Retries | Enabled |

Successful test evidence:

```text
Availability result: Successful
Availability location: Australia East
Duration: 1.7 seconds
```

This confirms that the deployed `/health/` endpoint is reachable from an external Azure monitoring location.

---

## Availability Alert Rule

An alert rule was automatically created for the Application Insights availability test.

Alert configuration:

| Field | Value |
|---|---|
| Scope | `<application-insights-name>` |
| Signal | Availability |
| Condition | Failed locations >= 2 |
| Severity | 1 - Error |
| Estimated cost | Approximately $0.10/month |
| Description | Automatically created alert rule for availability test `fastapi-health-check` |

This alert rule is acceptable for the portfolio project because it avoids alerting on a single temporary regional failure. It only triggers when multiple test locations fail.

---

## Action Group Notes

An extra custom action group was initially created and then deleted to keep the Azure setup clean.

Application Insights already created or used its own monitoring-related action group:

```text
Application Insights Smart Detection
```

The final setup keeps the monitoring configuration simple:

```text
Availability test
        ↓
Automatic availability alert rule
        ↓
Application Insights monitoring action group
```

---

## Monitoring Verification Script

Monitoring setup is verified using:

```powershell
python scripts\verify_azure_monitoring_setup.py
```

The script creates a verification report:

```text
data/processed/azure_monitoring_setup_verification_report.csv
```

The script verifies:

- App Service logging was manually enabled
- Log Stream was manually verified
- Built-in App Service Health Check is not used as the primary monitoring method
- Application Insights was created
- Availability test was created
- Availability alert rule was created
- Public health endpoint returns HTTP 200
- JWT login endpoint returns an access token
- Protected executive summary endpoint returns HTTP 200 when called with a valid JWT Bearer token
- Protected operational alert summary endpoint returns HTTP 200 when called with a valid JWT Bearer token

---

## Verification Report Columns

| Column | Description |
|---|---|
| `check_name` | Name of the monitoring or endpoint check |
| `component` | Azure or application component being checked |
| `expected_configuration` | Expected monitoring setup or endpoint behavior |
| `verification_method` | Manual or automated verification method |
| `url` | Endpoint URL tested, if applicable |
| `status_code` | HTTP status code returned by endpoint checks |
| `passed` | Boolean pass/fail result |
| `response_preview` | Short preview of endpoint response |
| `checked_at_utc` | UTC timestamp when the check was recorded |

---

## Health Endpoint

The deployed health endpoint is:

```text
/health/
```

Full URL:

```text
https://<app-service-hostname>/health/
```

Expected response:

```json
{
  "status": "ok",
  "service": "E-Commerce Retail Intelligence API",
  "database_connected": true
}
```

This endpoint is used by:

- Manual browser testing
- Application Insights availability testing
- Monitoring verification script

---

## Troubleshooting

### Availability test fails

Check:

- App Service is running
- `/health/` endpoint is reachable
- Azure SQL Database is online
- App Service environment variables are correct
- Key Vault references are resolved
- Container image is running successfully

---

### Log Stream shows no activity

Check:

- Application logging is enabled
- The app was restarted after enabling logs
- A request was made to `/health/`
- The container is running

---

### Protected endpoint checks fail

Check:

- Local `.env` contains the current JWT admin username and password
- Azure Key Vault contains the current JWT signing secret and demo user credentials
- App Service Key Vault references for JWT settings are resolved
- The request first authenticates through `/auth/login`
- The protected request uses the header `Authorization: Bearer <access_token>`
- API serving objects exist in Azure SQL

---

### Built-in Health Check not used

The project uses Application Insights availability tests instead of built-in App Service Health Check.

Application Insights availability testing is preferred here because it checks the public `/health/` endpoint externally from multiple Azure locations and provides monitoring evidence for the deployed API.

---

## Security and Governance Notes

The monitoring phase does not expose secrets.

The monitoring verification script uses the local `.env` file for JWT demo credentials. The `.env` file is ignored by Git and must not be committed.

Application Insights monitors the public `/health/` endpoint without requiring JWT authentication.

Protected endpoints are tested through JWT authentication by logging in through `/auth/login` and sending the returned access token with:

```text
Authorization: Bearer <access_token>
```

JWT signing secrets and demo user credentials are stored in Azure Key Vault for the deployed App Service.

---

## Phase Outcome

At the end of this phase, the platform has basic production-style observability.

The cloud platform now includes:

```text
Azure Blob Storage
        ↓
Azure Data Factory
        ↓
Azure SQL Database
        ↑
Azure Key Vault
        ↓
Azure App Service FastAPI API
        ↓
Application Insights Availability Monitoring
        ↓
Azure Monitor Alert Rule
```

This completes the monitoring and availability layer of the cloud deployment.
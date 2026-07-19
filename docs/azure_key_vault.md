# Azure Key Vault Secret Management

## Purpose

This phase adds Azure Key Vault to the E-Commerce Retail Intelligence Platform to improve cloud security and secret management.

Before this phase, sensitive runtime values such as Azure SQL credentials and API keys were stored directly as Azure App Service environment variable values.

After this phase, sensitive values are stored in Azure Key Vault. Azure App Service uses managed identity to access those secrets through Key Vault references.

The FastAPI application still reads values as normal environment variables, but Azure resolves those values securely from Key Vault at runtime.

---

## Secret Management Architecture

```text
Azure Key Vault
        ↓
Key Vault references in App Service settings
        ↓
Azure App Service managed identity
        ↓
FastAPI environment variables
        ↓
Azure SQL Database and protected API routes
```

---

## Azure Resources

| Resource Type | Resource Name |
|---|---|
| Resource Group | `rg-ecommerce-retail-intelligence` |
| Azure Key Vault | `kvretailmelbin` |
| Azure App Service | `app-ecommerce-retail-api-melbin` |
| Azure SQL Database | `sqldb-ecommerce-retail-intelligence` |
| Permission model | Azure role-based access control |

---

## Why Key Vault Was Added

Azure Key Vault was added to avoid storing sensitive values directly in application configuration.

This improves the project in several ways:

- Secrets are centralized in a secure Azure service.
- The application does not store secrets in source code.
- The `.env` file is not committed to GitHub.
- App Service reads secrets using managed identity.
- Azure role-based access control controls who and what can access secrets.
- Future secret rotation becomes easier.
- The project demonstrates a more professional cloud security pattern.

---

## Secrets Stored in Key Vault

The following secrets are stored in Azure Key Vault:

| Key Vault secret name | Purpose |
|---|---|
| `azure-sql-server` | Azure SQL Server hostname |
| `azure-sql-database` | Azure SQL Database name |
| `azure-sql-username` | Azure SQL login username |
| `azure-sql-password` | Azure SQL login password |
| `admin-api-key` | Admin API key for protected API endpoints |
| `analyst-api-key` | Analyst API key for analyst-level API access |
| `viewer-api-key` | Viewer API key for limited read-only API access |

Actual secret values are not documented and are not committed to GitHub.

---

## Managed Identity Access

The deployed App Service uses a system-assigned managed identity.

This identity is granted permission to read secrets from Key Vault.

| Identity | Azure Role | Scope |
|---|---|---|
| Developer Azure user | `Key Vault Secrets Officer` | Key Vault |
| App Service managed identity | `Key Vault Secrets User` | Key Vault |

The `Key Vault Secrets Officer` role allows the developer to create and manage secrets.

The `Key Vault Secrets User` role allows the App Service to read secret values at runtime.

---

## App Service Key Vault References

Azure App Service environment variables use Key Vault references.

The app setting names remain the same as before, but the values point to Key Vault secrets.

| App Service setting | Key Vault reference |
|---|---|
| `AZURE_SQL_SERVER` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-server)` |
| `AZURE_SQL_DATABASE` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-database)` |
| `AZURE_SQL_USERNAME` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-username)` |
| `AZURE_SQL_PASSWORD` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-password)` |
| `ADMIN_API_KEY` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=admin-api-key)` |
| `ANALYST_API_KEY` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=analyst-api-key)` |
| `VIEWER_API_KEY` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=viewer-api-key)` |

These settings are configured in:

```text
Azure Portal
→ App Services
→ app-ecommerce-retail-api-melbin
→ Settings
→ Environment variables
→ App settings
```

---

## Non-Secret App Service Settings

Some App Service settings are not sensitive and remain as plain values.

| App setting | Value |
|---|---|
| `APP_ENV` | `azure` |
| `AZURE_SQL_DRIVER` | `ODBC Driver 18 for SQL Server` |
| `WEBSITES_PORT` | `8000` |

---

## How the FastAPI App Uses Key Vault Values

The FastAPI code does not directly call Azure Key Vault.

Instead, Azure App Service resolves the Key Vault references and injects the resolved values as environment variables.

The application reads them using normal environment variable logic.

Example:

```text
App Service setting:
AZURE_SQL_PASSWORD=@Microsoft.KeyVault(...)

Runtime environment variable seen by FastAPI:
AZURE_SQL_PASSWORD=<resolved secret value>
```

This means the application code stays simple while the deployment becomes more secure.

---

## Runtime Flow

```text
1. Request reaches Azure App Service
2. App Service starts the Docker container
3. App Service resolves Key Vault references
4. FastAPI reads environment variables
5. API connects to Azure SQL Database
6. API validates request API keys
7. API returns business or operational response
```

---

## Verification

Key Vault setup is verified with:

```powershell
python scripts\verify_key_vault_setup.py
```

The script checks:

- Public health endpoint
- Protected executive summary endpoint
- Protected operational alert summary endpoint

The verification report is written to:

```text
data/processed/key_vault_setup_verification_report.csv
```

A successful result confirms that:

- The deployed API is still running.
- The API can connect to Azure SQL.
- Protected endpoints still accept the admin API key.
- Key Vault references are resolving correctly inside App Service.

---

## Expected Health Response

The health endpoint should return:

```json
{
  "status": "ok",
  "service": "E-Commerce Retail Intelligence API",
  "database_connected": true
}
```

If `database_connected` is `true`, the Azure SQL secret references are working.

If protected endpoints return HTTP 200 with the generated admin key, the API key secret reference is working.

---

## Troubleshooting

### Key Vault reference shows unresolved

Common causes:

- App Service managed identity does not have `Key Vault Secrets User`.
- RBAC permission has not propagated yet.
- Secret name is misspelled.
- Vault name is misspelled.
- Secret is disabled.
- App Service was not restarted after updating settings.

---

### Health endpoint returns database_connected false

Check:

- `AZURE_SQL_SERVER` reference
- `AZURE_SQL_DATABASE` reference
- `AZURE_SQL_USERNAME` reference
- `AZURE_SQL_PASSWORD` reference
- Azure SQL firewall settings
- Azure SQL database availability
- `APP_ENV=azure`

---

### Protected endpoints return 401 or 403

Check:

- The request uses the correct header: `X-API-Key`.
- The local `.env` contains the same generated admin key used in Key Vault.
- The `ADMIN_API_KEY` App Service setting resolves correctly.
- The App Service was restarted after changing the Key Vault reference.

---

## Security Notes

Current security improvements:

- SQL password is no longer stored directly in App Service configuration.
- API keys are no longer stored directly in App Service configuration.
- App Service uses managed identity to access secrets.
- Key Vault uses Azure RBAC permissions.
- Real secrets are not committed to GitHub.
- `.env.example` contains placeholders only.

Remaining limitations:

- The API still uses API key authentication rather than OAuth or Entra ID authentication.
- The Azure SQL connection still uses SQL username/password, now stored in Key Vault.
- Secret rotation is not automated.
- Full monitoring and alerting will be added in a later phase.

---

## Interview Explanation

Simple explanation:

```text
I added Azure Key Vault so sensitive values are no longer stored directly in the App Service configuration. The FastAPI App Service uses managed identity to read secrets from Key Vault through Key Vault references. This keeps the Python code simple because App Service resolves the secrets into environment variables at runtime.
```

Technical explanation:

```text
I configured Azure Key Vault using the Azure RBAC permission model. My developer account has Key Vault Secrets Officer permission to manage secrets, while the App Service system-assigned managed identity has Key Vault Secrets User permission to read them. App Service application settings use @Microsoft.KeyVault references for SQL credentials and API keys. The FastAPI container receives the resolved values as environment variables and connects to Azure SQL Database in APP_ENV=azure mode.
```

---

## Phase Outcome

At the end of this phase, the project has a stronger cloud security layer.

Updated architecture:

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
Authenticated business, operational, and insight endpoints
```

This phase demonstrates secure secret management, managed identity usage, and cloud runtime configuration.
# Azure Key Vault Secret Management

## Purpose

This phase adds Azure Key Vault to the E-Commerce Retail Intelligence Platform to improve cloud security and secret management.

Before this phase, sensitive runtime values such as Azure SQL credentials, JWT signing secrets, and authentication credentials could have been stored directly as Azure App Service environment variable values.

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
Azure SQL Database and JWT-protected API routes
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
- JWT signing secrets and demo user credentials are separated from source code and plain App Service configuration.

---

## Secrets Stored in Key Vault

The following secrets are stored in Azure Key Vault:

| Key Vault secret name | Purpose |
|---|---|
| `azure-sql-server` | Azure SQL Server hostname |
| `azure-sql-database` | Azure SQL Database name |
| `azure-sql-username` | Azure SQL login username |
| `azure-sql-password` | Azure SQL login password |
| `jwt-secret-key` | Secret key used to sign JWT access tokens |
| `jwt-admin-username` | Demo admin username |
| `jwt-admin-password` | Demo admin password |
| `jwt-analyst-username` | Demo analyst username |
| `jwt-analyst-password` | Demo analyst password |
| `jwt-viewer-username` | Demo viewer username |
| `jwt-viewer-password` | Demo viewer password |

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

The app setting names remain application-friendly, but the values point to Key Vault secrets.

| App Service setting | Key Vault reference |
|---|---|
| `AZURE_SQL_SERVER` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-server)` |
| `AZURE_SQL_DATABASE` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-database)` |
| `AZURE_SQL_USERNAME` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-username)` |
| `AZURE_SQL_PASSWORD` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=azure-sql-password)` |
| `JWT_SECRET_KEY` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-secret-key)` |
| `JWT_ADMIN_USERNAME` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-admin-username)` |
| `JWT_ADMIN_PASSWORD` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-admin-password)` |
| `JWT_ANALYST_USERNAME` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-analyst-username)` |
| `JWT_ANALYST_PASSWORD` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-analyst-password)` |
| `JWT_VIEWER_USERNAME` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-viewer-username)` |
| `JWT_VIEWER_PASSWORD` | `@Microsoft.KeyVault(VaultName=kvretailmelbin;SecretName=jwt-viewer-password)` |

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
| `JWT_ALGORITHM` | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |

---

## How the FastAPI App Uses Key Vault Values

The FastAPI code does not directly call Azure Key Vault.

Instead, Azure App Service resolves the Key Vault references and injects the resolved values as environment variables.

The application reads them using normal environment variable logic.

Example:

```text
App Service setting:
JWT_SECRET_KEY=@Microsoft.KeyVault(...)

Runtime environment variable seen by FastAPI:
JWT_SECRET_KEY=<resolved secret value>
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
6. User authenticates through POST /auth/login
7. API validates demo user credentials from resolved environment variables
8. API returns a signed JWT access token
9. Client sends Authorization: Bearer <access_token>
10. API validates the JWT token and role permissions
11. API returns business, operational, or insight response
```

---

## JWT Authentication Flow

```text
POST /auth/login
        ↓
Validate username and password
        ↓
Create JWT with username and role claims
        ↓
Return access token
        ↓
Client sends Authorization: Bearer <access_token>
        ↓
Protected route validates JWT
        ↓
RBAC dependency checks role permission
        ↓
Endpoint returns response
```

---

## JWT Roles

The API supports three demo JWT roles.

| Role | Access Level |
|---|---|
| `admin` | Full access to executive, operations, insights, and admin-level endpoints |
| `analyst` | Access to executive, operations, and insight endpoints |
| `viewer` | Limited summary-level read access |

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
- Key Vault references resolving correctly through App Service environment variables
- Azure SQL connectivity through resolved SQL secrets
- JWT authentication using resolved JWT credentials

The verification report is written to:

```text
data/processed/key_vault_setup_verification_report.csv
```

A successful result confirms that:

- The deployed API is running.
- The API can connect to Azure SQL.
- JWT Key Vault references are resolving correctly inside App Service.
- Protected endpoints accept valid JWT Bearer tokens.
- RBAC restrictions are active.

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

---

## Expected JWT Login Response

The login endpoint should return a JWT access token.

Endpoint:

```text
POST /auth/login
```

Example successful response:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "role": "admin",
  "expires_in_minutes": 60
}
```

If login succeeds using the credentials resolved from Key Vault, the JWT credential secret references are working.

---

## Example Protected Request

After login, protected endpoints require:

```text
Authorization: Bearer <access_token>
```

PowerShell example:

```powershell
$loginResponse = Invoke-RestMethod `
  -Method Post `
  -Uri "https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net/auth/login" `
  -ContentType "application/x-www-form-urlencoded" `
  -Body "username=admin&password=<admin-password>"

$headers = @{
    "Authorization" = "Bearer $($loginResponse.access_token)"
}

Invoke-RestMethod `
  -Uri "https://app-ecommerce-retail-api-melbin-a9habdejcgf0fkha.francecentral-01.azurewebsites.net/executive/summary" `
  -Headers $headers
```

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

### JWT login returns 401

Check:

- The username matches the Key Vault value.
- The password matches the Key Vault value.
- The App Service setting points to the correct Key Vault secret.
- The App Service managed identity can read the JWT credential secrets.
- The App Service was restarted after adding or changing JWT Key Vault references.
- The request uses `Content-Type: application/x-www-form-urlencoded`.
- The login request is sent to `/auth/login`.

---

### Protected endpoints return 401

Check:

- The request includes the header:

```text
Authorization: Bearer <access_token>
```

- The token was copied correctly.
- The token has not expired.
- `JWT_SECRET_KEY` is resolving correctly from Key Vault.
- The app was restarted after changing `JWT_SECRET_KEY`.

---

### Protected endpoints return 403

Check:

- The authenticated user role has permission for the endpoint.
- `viewer` users only have limited summary-level read access.
- `analyst` users do not have admin-only access.
- `/insights/llm-context` requires the `admin` role.

---

## Security Notes

Current security improvements:

- SQL password is no longer stored directly in App Service configuration.
- JWT signing secret is stored in Azure Key Vault.
- JWT demo user credentials are stored in Azure Key Vault.
- App Service uses managed identity to access secrets.
- Key Vault uses Azure RBAC permissions.
- Real secrets are not committed to GitHub.
- `.env.example` contains placeholders only.
- Protected endpoints use JWT Bearer authentication with RBAC.

Remaining limitations:

- The API uses demo JWT users rather than a production identity provider.
- The API does not use Microsoft Entra ID authentication.
- Refresh tokens are not implemented.
- User registration and password reset are not implemented.
- The Azure SQL connection still uses SQL username/password, now stored in Key Vault.
- Secret rotation is not automated.

These limitations are intentional for this portfolio project because the goal is to demonstrate production-style cloud security patterns without overcomplicating the system.

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
JWT-protected business, operational, and insight endpoints
```

This phase demonstrates secure secret management, managed identity usage, JWT-based API authentication, role-based authorization, and cloud runtime configuration.
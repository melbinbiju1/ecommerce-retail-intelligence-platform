from time import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.logging_config import api_logger
from src.api.routes.health import router as health_router
from src.api.routes.executive import router as executive_router
from src.api.routes.operations import router as operations_router
from src.api.routes.insights import router as insights_router


app = FastAPI(
    title="E-Commerce Retail Intelligence API",
    description=(
        "FastAPI backend for serving executive KPIs, sales trends, "
        "operational anomaly alerts, AI-ready business insights, "
        "and risk summaries from the E-Commerce Retail Intelligence Platform."
    ),
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()

    try:
        response = await call_next(request)
        duration_ms = round((time() - start_time) * 1000, 2)

        api_logger.info(
            f"{request.method} {request.url.path} | "
            f"status={response.status_code} | duration_ms={duration_ms}"
        )

        return response

    except Exception as error:
        duration_ms = round((time() - start_time) * 1000, 2)

        api_logger.exception(
            f"{request.method} {request.url.path} failed | "
            f"duration_ms={duration_ms} | error={error}"
        )

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error. Check API logs for details.",
            },
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    api_logger.exception(f"Unhandled error on {request.url.path}: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Unexpected server error. Check API logs for details.",
        },
    )


app.include_router(health_router)
app.include_router(executive_router)
app.include_router(operations_router)
app.include_router(insights_router)


@app.get("/")
def root() -> dict:
    return {
        "message": "E-Commerce Retail Intelligence API",
        "docs": "/docs",
        "health": "/health",
        "system_status": "/health/status",
        "authentication": "Use X-API-Key header for protected endpoints.",
        "demo_roles": {
            "admin": "Full access",
            "analyst": "Executive and operational read access",
            "viewer": "Limited executive read access",
        },
    }
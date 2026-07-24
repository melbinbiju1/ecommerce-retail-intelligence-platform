from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import auth
from src.api.routes import health
from src.api.routes import executive
from src.api.routes import operations
from src.api.routes import insights


app = FastAPI(
    title="E-Commerce Retail Intelligence API",
    description=(
        "Secured analytics API for executive KPIs, operational anomaly "
        "detection, and AI-ready business insights."
    ),
    version="1.0.0",
    contact={
        "name": "Melbin Biju",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "E-Commerce Retail Intelligence API",
        "status": "running",
        "docs": "/docs",
        "health": "/health/",
        "authentication": "/auth/login",
    }


app.include_router(auth.router)
app.include_router(health.router)
app.include_router(executive.router)
app.include_router(operations.router)
app.include_router(insights.router)
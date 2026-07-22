from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.routers import ads
from app.models import HealthCheckResponse
from app.utils.logger import logger

app = FastAPI(
    title="Claude Meta Ads Tool",
    description="API for searching Meta ads and analyzing them with Claude AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )

app.include_router(ads.router, prefix=f"/api/{settings.api_version}")

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0"
    )

@app.get("/")
async def root():
    return {
        "service": "Claude Meta Ads Tool",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("API startup")
    logger.info(f"API Version: {settings.api_version}")
    logger.info(f"Debug Mode: {settings.debug}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API shutdown")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

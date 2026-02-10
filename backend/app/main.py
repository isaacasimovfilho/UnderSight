from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.security import decode_access_token
from app.core.middlewares import TenantContext
from app.api import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="SIEM Nova Geração - Security Information and Event Management",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Tenant Middleware
    @app.middleware("http")
    async def tenant_context_middleware(request: Request, call_next):
        # Extract token from header
        token = request.headers.get("Authorization")
        
        if token and token.startswith("Bearer "):
            try:
                payload = decode_access_token(token.replace("Bearer ", ""))
                if payload:
                    TenantContext.set(
                        tenant_id=payload.get("tenant_id", "default"),
                        tenant_type=payload.get("tenant_type", "customer")
                    )
            except Exception:
                pass
        
        response = await call_next(request)
        TenantContext.clear()
        return response
    
    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    
    # Health check (public)
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "version": settings.app_version,
            "timestamp": "2026-02-09T05:00:00Z"
        }
    
    @app.get("/")
    async def root():
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "docs": "/docs"
        }
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )

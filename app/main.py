"""
FastAPI main application for Restaurant Management System.
"""
import os
import logging
from datetime import datetime
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from database import engine, get_db
from routes import categorias, meseros, mesas, menu_productos, ordenes, detalles_orden
import schemas

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Restaurant Management API",
    description="API REST completa para sistema de gestión de restaurante",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", response_model=schemas.HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API and database connectivity.
    """
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "timestamp": datetime.utcnow()
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "Restaurant Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else "An error occurred"
        }
    )


# Register routers
app.include_router(categorias.router, prefix="/api/v1")
app.include_router(meseros.router, prefix="/api/v1")
app.include_router(mesas.router, prefix="/api/v1")
app.include_router(menu_productos.router, prefix="/api/v1")
app.include_router(ordenes.router, prefix="/api/v1")
app.include_router(detalles_orden.router, prefix="/api/v1")


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Runs on application startup.
    """
    logger.info("Starting Restaurant Management API...")
    logger.info(f"Database server: {os.getenv('DB_SERVER', 'Not configured')}")
    logger.info(f"Database name: {os.getenv('DB_NAME', 'Not configured')}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs on application shutdown.
    """
    logger.info("Shutting down Restaurant Management API...")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("RELOAD", "false").lower() == "true"
    )

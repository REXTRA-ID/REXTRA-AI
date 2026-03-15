# app/main.py
"""
Main Application
"""
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.api.v1.router import api_v1_router
from app.db.session import engine
from app.db.base import Base
from app.core.config import settings

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

from app.shared.ai_client import gemini_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler"""
    logger.info("Starting Career Profile API...")
    
    # --- DATABASE SNITCH START ---
    from app.db.session import SessionLocal
    from sqlalchemy import text
    from app.core.config import settings
    
    print("\n" + "!"*60)
    print(f"!!! DATABASE SNITCH !!!")
    print(f"URL DARI SETTINGS: {settings.DATABASE_URL}")
    
    db = SessionLocal()
    try:
        res = db.execute(text("SELECT count(*) FROM user_career_profiles")).fetchone()
        print(f"ISI TABEL user_career_profiles: {res[0]} baris")
        
        # Cek data terakhir
        rows = db.execute(text("SELECT id, user_id, is_active FROM user_career_profiles ORDER BY id DESC LIMIT 5")).fetchall()
        for r in rows:
            print(f"  - ID: {r[0]} | User: {r[1]} | Active: {r[2]}")
    except Exception as e:
        print(f"!!! GAGAL CEK DB: {e}")
    finally:
        db.close()
    print("!"*60 + "\n")
    # --- DATABASE SNITCH END ---

    # Create database tables if they don't exist
    # NOTE: In production, use Alembic migrations instead
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created")
    except Exception as e:
        logger.error(f"Failed to create tables: {str(e)}")
    
    logger.info("Career Profile API started successfully")
    
    yield
    
    logger.info("Shutting down Career Profile API...")


# Create FastAPI application
app = FastAPI(
    title="Career Profile API",
    description="RIASEC Assessment and Career Profiling System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(api_v1_router)

REQUEST_COUNT = Counter("app_requests_total", "Total request count")

# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Database error occurred",
            "error": str(exc)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc)
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API welcome message
    """
    REQUEST_COUNT.inc()
    return {
        "message": "Welcome to Career Profile API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/api/v1/health",
        "api_endpoints": "/api/v1/"
    }

from app.shared.ai_client import gemini_client


# @app.get("/test")
# async def test_ai():
#     try:
#         # Menyiapkan pesan dalam format list of dict
#         messages = [
#             {"role": "user", "content": "Halo, siapa kamu?"}
#         ]
#
#         # Memanggil method chat_completion dengan await
#         response_text = await gemini_client.chat_completion(
#             messages=messages,
#             dimension="test_endpoint"  # Untuk tracking prometheus kamu
#         )
#
#         return {
#             "status": "success",
#             "ai_response": response_text
#         }
#
#     except Exception as e:
#         # Jika semua retry gagal, tangkap error-nya
#         raise HTTPException(status_code=500, detail=str(e))
#
#

from app.shared.cache import cache_set, cache_get
@app.get("/test-redis")
def test_redis_connection():
    try:
        # 1. Coba simpan data
        test_data = {"status": "ok", "message": "Redis is working!"}
        cache_set("debug_key", test_data, ttl=60)

        # 2. Coba ambil data
        retrieved_data = cache_get("debug_key")

        if retrieved_data == test_data:
            return {"status": "success", "data": retrieved_data}
        return {"status": "error", "message": "Data mismatch"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Endpoint /metrics
@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint

    Returns the API status and version information.
    """
    return {
        "status": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "Healthy"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Disable in production
        log_level="info"
    )
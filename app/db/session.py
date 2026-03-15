from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from typing import Generator

DATABASE_URL = settings.DATABASE_URL

# pool_recycle diambil dari settings (default 1800 = 30 menit)
# Brief RIASEC halaman 102: pool_recycle=settings.DB_POOL_RECYCLE
# Penting untuk DB remote: koneksi stale di-recycle sebelum timeout dari sisi server
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,                          # Verify connections before using
    pool_size=settings.SQLALCHEMY_POOL_SIZE,
    max_overflow=settings.SQLALCHEMY_MAX_OVERFLOW,
    echo=False,                                  # Set to True untuk debug SQL (dev only)
    pool_timeout=30,
    pool_recycle=settings.DB_POOL_RECYCLE        # 1800 detik = 30 menit
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function untuk FastAPI endpoints.

    Menyediakan database session dan memastikan session ditutup
    setelah request selesai.

    Usage:
        @app.get("/example")
        def example(db: Session = Depends(get_db)):
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_context():
    """
    Context manager untuk database session di luar FastAPI
    (scripts, background tasks).

    Usage:
        with get_db_context() as db:
            pass
    """
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
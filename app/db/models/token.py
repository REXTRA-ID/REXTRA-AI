# app/db/models/token.py
# Model ini membaca tabel milik Golang — JANGAN buat migrasi untuk tabel ini.
# Alembic hanya untuk tabel milik FastAPI.

from sqlalchemy import Column, String, Integer, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

class TokenWallet(Base):
    __tablename__ = "token_wallet"
    __table_args__ = {"schema": "public"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    balance = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True))


class TokenLedger(Base):
    __tablename__ = "token_ledger"
    __table_args__ = {"schema": "public"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    occurred_at = Column(DateTime(timezone=True), nullable=False)
    wallet_id = Column(UUID(as_uuid=True), nullable=False)
    direction = Column(String(3), nullable=False)
    amount = Column(Integer, nullable=False)
    balance_before = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)
    source_type = Column(String(100))
    source_id = Column(BigInteger, nullable=True)    # FIX 1: DB pakai bigint bukan UUID
    reference_id = Column(UUID(as_uuid=True))
    description = Column(String(500))
    metadata_ = Column("metadata", String, nullable=True, server_default="'{}'")  # FIX 2: nullable
    operator_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), nullable=False)
    ref = Column(String)
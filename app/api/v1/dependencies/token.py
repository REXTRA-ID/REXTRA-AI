# app/api/v1/dependencies/token.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models.token import TokenWallet, TokenLedger
from app.db.models.user import User
from datetime import datetime, timezone
import uuid

TOKEN_COST_RECOMMENDATION = 3

def check_and_deduct_token(
    user: User,
    db: Session,
    amount: int = TOKEN_COST_RECOMMENDATION,
    description: str = "Pemakaian Tes Profil Karier"
) -> TokenWallet:
    """
    Cek saldo token dan kurangi jika mencukupi.
    Update token_wallet dan tambah baris baru di token_ledger.
    """
    wallet = db.query(TokenWallet).filter(
        TokenWallet.user_id == user.id
    ).with_for_update().first()

    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token wallet user tidak ditemukan"
        )

    if wallet.balance < amount:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=(
                f"Token tidak mencukupi. "
                f"Saldo: {wallet.balance} token, dibutuhkan: {amount} token."
            )
        )

    balance_before = wallet.balance
    balance_after  = wallet.balance - amount

    wallet.balance    = balance_after
    wallet.updated_at = datetime.now(timezone.utc)

    ledger_entry = TokenLedger(
        id             = uuid.uuid4(),
        occurred_at    = datetime.now(timezone.utc),
        wallet_id      = wallet.id,
        direction      = "OUT",
        amount         = amount,
        balance_before = balance_before,
        balance_after  = balance_after,
        # FIX: Golang entity mendefinisikan source_type varchar(12) dengan valid values:
        # TOPUP | MEMBERSHIP | USAGE | ADJUSTMENT | REFUND | EXPIRED
        # "CAREER_PROFILE_TEST" = 19 karakter → melebihi varchar(12) → DB error!
        source_type    = "USAGE",
        source_id      = None,          # bigint nullable
        description    = description,
        metadata_      = "{}",          # NOT NULL di DB, isi JSON kosong
        created_at     = datetime.now(timezone.utc)
    )
    db.add(ledger_entry)

    return wallet
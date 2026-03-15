# app/api/v1/dependencies/auth.py
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User
import uuid

ALLOWED_ROLES = {"USER", "EXPERT"}

async def get_current_user(
    x_user_id: str = Header(..., description="UUID user dari JWT yang sudah divalidasi Golang"),
    db: Session = Depends(get_db)
) -> User:
    """
    Ambil user dari DB berdasarkan x-user-id di header.
    
    Catatan implementasi:
    Header x-user-id dikirim Flutter setelah JWT divalidasi di Golang service.
    Untuk production yang lebih ketat, FastAPI bisa memvalidasi JWT secara mandiri
    menggunakan shared secret atau public key dari Golang auth service.
    Untuk sekarang, user_id di-lookup langsung ke database.
    """
    try:
        user_uuid = uuid.UUID(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Format user ID tidak valid"
        )

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User tidak ditemukan"
        )
    return user


async def require_career_test_role(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Pastikan user punya role yang diizinkan untuk tes profil karier.
    Role yang diizinkan: USER, EXPERT.
    """
    if current_user.role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role '{current_user.role}' tidak memiliki akses ke tes profil karier"
        )
    return current_user


async def require_active_membership(
    current_user: User = Depends(require_career_test_role),
    db: Session = Depends(get_db)
) -> User:
    """
    Cek status membership user.
    
    === TODO: IMPLEMENTASI MEMBERSHIP (BELUM AKTIF) ===
    
    File yang perlu dimodifikasi saat diaktifkan:
    - app/db/models/membership.py  → tambah model UserMembership
    - app/api/v1/dependencies/auth.py → file ini, aktifkan logika di bawah
    
    Langkah implementasi:
    1. Konfirmasi nama tabel membership dengan tim Golang
       (kemungkinan: user_memberships / subscriptions / user_plans)
    2. Buat model SQLAlchemy di app/db/models/membership.py
    3. Query:
       membership = db.query(UserMembership).filter(
           UserMembership.user_id == current_user.id,
           UserMembership.status == "ACTIVE",
           UserMembership.expired_at > datetime.utcnow()
       ).first()
       if not membership:
           raise HTTPException(status_code=403, detail="Membership tidak aktif atau sudah expired")
    
    Untuk sekarang: semua user yang sudah lolos role check dianggap memiliki membership sah.
    """
    # TODO: Aktifkan pengecekan membership setelah nama tabel dikonfirmasi
    return current_user

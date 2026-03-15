import json
import logging
import redis
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

# ── Inisialisasi client ───────────────────────────────────────────────────────
# redis_client bisa bernilai None jika koneksi gagal saat startup.
# Semua fungsi di bawah sudah menangani kasus None ini.
try:
    redis_client = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=2,    # Gagal cepat jika Redis tidak bisa dicapai
        socket_timeout=2,
    )
    # Ping untuk validasi koneksi awal
    redis_client.ping()
except Exception as e:
    logger.warning(f"Redis tidak tersedia saat startup: {e}. Cache akan di-skip.")
    redis_client = None


# ── Fungsi helper publik ──────────────────────────────────────────────────────

def cache_get(key: str) -> Optional[dict]:
    """
    Ambil value dari Redis dan parse sebagai dict.
    Return None jika Redis down, key tidak ada, atau value bukan JSON valid.
    """
    raw = cache_get_raw(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


def cache_set(key: str, value: dict, ttl: int = 3600) -> bool:
    """
    Simpan dict ke Redis sebagai JSON string dengan TTL.
    Return True jika berhasil, False jika Redis down atau error.
    """
    try:
        serialized = json.dumps(value)
    except (TypeError, ValueError) as e:
        logger.warning(f"cache_set: gagal serialize value untuk key '{key}': {e}")
        return False
    return cache_set_raw(key, serialized, ttl=ttl)


def cache_get_raw(key: str) -> Optional[str]:
    """
    Ambil value mentah (string) dari Redis.
    Return None jika Redis down atau key tidak ada.
    Digunakan oleh ikigai_service yang menyimpan JSON string langsung.
    """
    if redis_client is None:
        return None
    try:
        return redis_client.get(key)
    except Exception as e:
        logger.warning(f"cache_get_raw: Redis error untuk key '{key}': {e}")
        return None


def cache_set_raw(key: str, value: str, ttl: int = 3600) -> bool:
    """
    Simpan string mentah ke Redis dengan TTL.
    Return True jika berhasil, False jika Redis down atau error.
    """
    if redis_client is None:
        return False
    try:
        redis_client.setex(key, ttl, value)
        return True
    except Exception as e:
        logger.warning(f"cache_set_raw: Redis error untuk key '{key}': {e}")
        return False


def cache_delete(key: str) -> bool:
    """
    Hapus key dari Redis.
    Return True jika berhasil, False jika Redis down atau error.
    """
    if redis_client is None:
        return False
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.warning(f"cache_delete: Redis error untuk key '{key}': {e}")
        return False
"""
app/seeders/profession_sub_category_seeder.py
----------------------------------------------
Seeder untuk tabel profession_sub_categories.
Idempotent — aman dijalankan ulang.

Cara menjalankan (dari root project):
    python -m app.seeders.profession_sub_category_seeder

Pastikan profession_main_category_seeder sudah dijalankan lebih dulu.
"""

import asyncio
from datetime import datetime, timezone
from sqlalchemy import select
from app.database.config import AsyncSessionLocal
from app.models.profession_main_category import ProfessionMainCategory
from app.models.profession_sub_category import ProfessionSubCategory

# Format: (main_category_code, sub_code, sub_name, description)
SUB_CATEGORIES = [
    # ── ENGINEERING ────────────────────────────────────────────────────────────
    ("ENGINEERING", "BACKEND",          "Backend",          "Profesi engineering yang membangun dan merawat sisi server aplikasi, termasuk logika bisnis, basis data, dan API."),
    ("ENGINEERING", "FRONTEND",         "Frontend",         "Profesi engineering yang membangun antarmuka aplikasi di sisi pengguna dan menerjemahkan rancangan tampilan menjadi kode interaktif dan responsif."),
    ("ENGINEERING", "MOBILE",           "Mobile",           "Profesi engineering yang mengembangkan aplikasi pada perangkat bergerak (Android/iOS) serta menjaga kompatibilitas dan performa lintas perangkat."),
    ("ENGINEERING", "DEVOPS",           "DevOps",           "Profesi engineering yang mengelola proses rilis dan penyebaran aplikasi, termasuk otomasi CI/CD dan pemantauan stabilitas sistem."),
    ("ENGINEERING", "QUALITY_ASSURANCE","Quality Assurance","Profesi engineering yang memverifikasi kualitas perangkat lunak sebelum rilis melalui pengujian fungsional dan otomatis."),
    ("ENGINEERING", "SECURITY",         "Security",         "Profesi engineering yang melindungi sistem dan data dari ancaman siber melalui penilaian kerentanan dan respons insiden."),
    ("ENGINEERING", "NETWORK",          "Network",          "Profesi engineering yang merancang dan memelihara jaringan komunikasi agar konektivitas stabil dan aman."),
    ("ENGINEERING", "GAME",             "Game",             "Profesi engineering yang membangun sistem permainan digital, termasuk logika interaksi dan integrasi aset grafis/audio."),
    ("ENGINEERING", "EMBEDDED",         "Embedded",         "Profesi engineering yang mengembangkan perangkat lunak pada sistem tertanam (firmware) dan perangkat IoT."),
    ("ENGINEERING", "ROBOTICS",         "Robotics",         "Profesi engineering yang merancang sistem robotik, termasuk algoritma kontrol dan integrasi sensor untuk otomasi industri."),
    ("ENGINEERING", "CLOUD",            "Cloud",            "Profesi engineering yang merancang dan mengelola layanan berbasis cloud, mencakup arsitektur, skalabilitas, dan efisiensi biaya."),
    ("ENGINEERING", "AUTOMATION",       "Automation",       "Profesi engineering yang membangun otomasi proses teknis untuk mengurangi human error dan mempercepat waktu rilis."),
    ("ENGINEERING", "HARDWARE",         "Hardware",         "Profesi engineering yang merancang dan mengembangkan perangkat keras untuk produk teknologi, termasuk pengujian prototipe dan integrasi software."),
    # ── DATA ───────────────────────────────────────────────────────────────────
    ("DATA", "INFRASTRUCTURE", "Infrastructure", "Kategori profesi yang berfokus pada pembangunan dan pengelolaan infrastruktur data, termasuk data pipeline dan penyimpanan data warehouse/data lake."),
    ("DATA", "GOVERNANCE",     "Governance",     "Kategori profesi yang berfokus pada pengelolaan kualitas data, kepatuhan regulasi, dan keamanan data."),
    ("DATA", "ANALYTICS",      "Analytics",      "Kategori profesi yang berfokus pada analisis data historis untuk menghasilkan wawasan pengambilan keputusan bisnis."),
    ("DATA", "SCIENCE",        "Science",        "Kategori profesi yang berfokus pada prediksi berbasis data menggunakan teknik statistik dan machine learning."),
    ("DATA", "AI",             "AI",             "Kategori profesi yang berfokus pada pengembangan sistem machine learning dan kemampuan kognitif buatan."),
    # ── PRODUCT ────────────────────────────────────────────────────────────────
    ("PRODUCT", "MANAGEMENT", "Management", "Kategori profesi yang bertanggung jawab atas visi, strategi, prioritas fitur, dan eksekusi peluncuran produk."),
    ("PRODUCT", "GROWTH",     "Growth",     "Kategori profesi yang fokus pada akuisisi pengguna, retensi, dan optimasi produk untuk meningkatkan konversi dan pendapatan."),
    ("PRODUCT", "OPERATIONS", "Operations", "Kategori profesi yang berfokus pada efisiensi proses dan ritme kerja dalam tim produk."),
    ("PRODUCT", "ANALYTICS",  "Analytics",  "Kategori profesi yang bertanggung jawab untuk analisis perilaku pengguna dan wawasan data produk."),
    # ── DESIGN ─────────────────────────────────────────────────────────────────
    ("DESIGN", "UI_UX",   "UI/UX",    "Subkategori profesi yang bertanggung jawab atas perancangan antarmuka pengguna (UI) dan pengalaman pengguna (UX)."),
    ("DESIGN", "VISUAL",  "Visual",   "Subkategori yang berfokus pada komunikasi visual, branding, dan desain grafis untuk memperkuat identitas merek digital."),
    ("DESIGN", "RESEARCH","Research", "Subkategori yang bertanggung jawab untuk meneliti perilaku pengguna melalui wawancara, survei, dan usability testing."),
    ("DESIGN", "CONTENT", "Content",  "Subkategori yang berfokus pada penulisan microcopy dan teks dalam produk digital untuk membantu navigasi pengguna."),
]


async def seed_profession_sub_category() -> None:
    async with AsyncSessionLocal() as session:
        # [FIX-5] Hanya ENGINEERING, DATA, PRODUCT, DESIGN yang di-cache karena
        # hanya 4 main category tersebut yang memiliki sub_category di data awal.
        # Main category lain (MARKETING, BUSINESS, FINANCE, PEOPLE, OPERATIONS, LEGAL)
        # belum memiliki sub_category — akan ditambahkan di iterasi data berikutnya.
        main_cache: dict[str, int] = {}
        for main_code in ("ENGINEERING", "DATA", "PRODUCT", "DESIGN"):
            result = await session.execute(
                select(ProfessionMainCategory).where(ProfessionMainCategory.code == main_code)
            )
            main = result.scalar_one_or_none()
            if main is None:
                raise RuntimeError(f"Main category '{main_code}' tidak ditemukan. Jalankan main category seeder dulu.")
            main_cache[main_code] = main.id

        for main_code, sub_code, sub_name, desc in SUB_CATEGORIES:
            main_id = main_cache[main_code]
            existing = await session.execute(
                select(ProfessionSubCategory).where(
                    ProfessionSubCategory.main_category_id == main_id,
                    ProfessionSubCategory.code == sub_code,
                )
            )
            if existing.scalar_one_or_none() is not None:
                print(f"[SKIP] {main_code}/{sub_code} — sudah ada")
                continue

            now = datetime.now(timezone.utc)
            session.add(ProfessionSubCategory(
                main_category_id=main_id,
                code=sub_code,
                name=sub_name,
                description=desc,
                created_at=now,
                updated_at=now,
            ))
            print(f"[INSERT] {main_code}/{sub_code}")

        await session.commit()
        print("✅ Seeder profession_sub_category selesai.")


if __name__ == "__main__":
    asyncio.run(seed_profession_sub_category())

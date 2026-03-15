"""
app/seeders/profession_main_category_seeder.py
------------------------------------------------
Seeder untuk tabel profession_main_categories.
Menggunakan pola "insert jika belum ada" (idempotent / safe to re-run).

Cara menjalankan (dari root project):
    python -m app.seeders.profession_main_category_seeder
"""

import asyncio
from datetime import datetime, timezone
from sqlalchemy import select
from app.database.config import AsyncSessionLocal
from app.models.profession_main_category import ProfessionMainCategory

CATEGORIES = [
    ("ENGINEERING", "Engineering",  "Kategori profesi teknis yang bertanggung jawab atas perancangan, pengembangan, pengujian, dan pemeliharaan sistem digital."),
    ("DATA",        "Data",         "Kategori profesi analitis yang berfokus pada pengumpulan, pengolahan, dan analisis data untuk menghasilkan wawasan strategis."),
    ("PRODUCT",     "Product",      "Kategori profesi strategis yang menjembatani aspek teknis, bisnis, dan desain dalam pengelolaan produk digital."),
    ("DESIGN",      "Design",       "Kategori profesi kreatif yang berfokus pada perancangan antarmuka dan pengalaman pengguna."),
    ("MARKETING",   "Marketing",    "Kategori profesi komunikasi yang berfokus pada promosi, branding, dan akuisisi pengguna."),
    ("BUSINESS",    "Business",     "Kategori profesi komersial yang berfokus pada strategi pertumbuhan dan kemitraan."),
    ("FINANCE",     "Finance",      "Kategori profesi manajerial yang mengelola kesehatan finansial dan strategi pendanaan perusahaan."),
    ("PEOPLE",      "People",       "Kategori profesi organisasi yang mengelola siklus hidup talenta dan budaya kerja."),
    ("OPERATIONS",  "Operations",   "Kategori profesi eksekusi yang memastikan efisiensi proses bisnis dan operasional."),
    ("LEGAL",       "Legal",        "Kategori profesi hukum yang menangani kepatuhan regulasi dan mitigasi risiko hukum."),
]


async def seed_profession_main_category() -> None:
    async with AsyncSessionLocal() as session:
        for code, name, description in CATEGORIES:
            existing = await session.execute(
                select(ProfessionMainCategory).where(ProfessionMainCategory.code == code)
            )
            if existing.scalar_one_or_none() is not None:
                print(f"[SKIP] {code} — sudah ada")
                continue

            now = datetime.now(timezone.utc)
            session.add(ProfessionMainCategory(
                code=code, name=name, description=description,
                created_at=now, updated_at=now,
            ))
            print(f"[INSERT] {code}")

        await session.commit()
        print("✅ Seeder profession_main_category selesai.")


if __name__ == "__main__":
    asyncio.run(seed_profession_main_category())

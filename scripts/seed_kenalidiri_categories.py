from sqlalchemy import text

from app.db.session import SessionLocal


def seed_kenalidiri_categories():
    db = SessionLocal()

    try:
        db.execute(
            text("""
            INSERT INTO kenalidiri_categories (
                id,
                category_code,
                category_name,
                description,
                detail_table_name,
                is_active
            )
            VALUES (
                1,
                'CAREER_PROFILE',
                'Tes Profil Karier',
                'Tes untuk mengetahui profil kepribadian karier (RIASEC) dan rekomendasi profesi yang sesuai (Ikigai)',
                'careerprofile_test_sessions',
                TRUE
            )
            ON CONFLICT (category_code) DO NOTHING;
            """)
        )

        db.execute(
            text("""
            SELECT setval(
                'kenalidiri_categories_id_seq',
                (SELECT MAX(id) FROM kenalidiri_categories),
                true
            );
            """)
        )

        db.commit()
        print("✅ kenalidiri_categories seeded successfully")

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


if __name__ == "__main__":
    seed_kenalidiri_categories()

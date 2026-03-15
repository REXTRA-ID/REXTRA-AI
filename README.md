```
kenali-diri-api/
├── .env
├── .env.example
├── API_EXAMPLES.md
├── alembic/
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   ├── versions/
│   │   ├── 995c97fff635_initial_migration.py
├── alembic.ini
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── categories/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── career_profile/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── models/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── profession.py
│   │   │   │   │   │   ├── riasec.py
│   │   │   │   │   │   ├── session.py
│   │   │   │   │   ├── repositories/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── profession_repo.py
│   │   │   │   │   │   ├── riasec_repo.py
│   │   │   │   │   │   ├── session_repo.py
│   │   │   │   │   ├── routers/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── session.py
│   │   │   │   │   ├── schemas/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── riasec.py
│   │   │   │   │   │   ├── session.py
│   │   │   │   │   ├── services/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── profession_expansion.py
│   │   │   │   │   │   ├── session_service.py
│   │   │   ├── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── kenalidiri_category.py
│   │   │   ├── kenalidiri_history.py
│   │   ├── session.py
│   ├── main.py
├── pyproject.toml
├── requirements.txt
├── scripts/
│   ├── clean.sql
│   ├── riasec_codes_complete_156.sql
│   ├── riasec_codes_complete_156.sql:Zone.Identifier
│   ├── riasec_codes_seeder.sql
│   ├── seed_kenalidiri_categories.py
```
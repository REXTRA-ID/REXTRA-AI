import os
import json
import sys
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal
from app.api.v1.categories.career_profile.models.riasec import RIASECQuestionSet

def import_riasec_questions():
    db: Session = SessionLocal()
    file_path = "data/riasec_questions.json"
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} tidak ditemukan!")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        set_version = data.get("set_version", "v1")
        questions_list = data.get("questions", [])

        if not questions_list:
            print("Error: Tidak ada data pertanyaan di dalam file JSON.")
            return

        print(f"Memproses {len(questions_list)} pertanyaan untuk versi {set_version}...")

        # 1. Nonaktifkan set lama
        db.query(RIASECQuestionSet).filter(
            RIASECQuestionSet.is_active == True
        ).update({"is_active": False})

        # 2. Cek apakah versi ini sudah ada
        existing_set = db.query(RIASECQuestionSet).filter(
            RIASECQuestionSet.set_version == set_version
        ).first()

        if existing_set:
            print(f"Versi {set_version} ditemukan. Melakukan update data...")
            existing_set.questions_data = questions_list
            existing_set.is_active = True
        else:
            print(f"Membuat set pertanyaan baru versi {set_version}...")
            new_set = RIASECQuestionSet(
                set_version=set_version,
                questions_data=questions_list,
                is_active=True
            )
            db.add(new_set)

        db.commit()
        print(f"SUKSES: 72 pertanyaan RIASEC berhasil diimpor sebagai '{set_version}'.")

    except Exception as e:
        print(f"Terjadi error saat impor: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_riasec_questions()
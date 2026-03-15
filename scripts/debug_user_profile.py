# debug_user_profile.py
import uuid
from app.db.session import SessionLocal
from app.api.v1.categories.career_profile.services.user_career_profile_service import UserCareerProfileService
from app.api.v1.categories.career_profile.models.user_career_profile import UserCareerProfile
from app.db.models.user import User

def debug_get_profile():
    db = SessionLocal()
    try:
        # Cari user yang punya profil aktif
        active_profile = db.query(UserCareerProfile).filter(UserCareerProfile.is_active == True).first()
        
        if not active_profile:
            print("Tidak ada profil aktif di DB.")
            return

        user_id = active_profile.user_id
        print(f"Mencoba get_active_profile untuk user_id: {user_id}")
        
        svc = UserCareerProfileService(db)
        result = svc.get_active_profile(user_id)
        print("Berhasil:", result)
        
    except Exception as e:
        import traceback
        print("ERROR TERDETEKSI:")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_get_profile()

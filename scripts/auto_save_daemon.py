# scripts/auto_save_daemon.py
import psycopg2
import os
import time
from dotenv import load_dotenv

load_dotenv()

def run_daemon():
    db_url = os.getenv("DATABASE_URL")
    print(f"[*] Auto-Save Daemon started. Connecting to: {db_url}")
    
    while True:
        conn = None
        try:
            conn = psycopg2.connect(db_url)
            cur = conn.cursor()
            
            # 1. Cari sesi completed yang belum ada di user_career_profiles
            # Kita join dengan riasec_results dan career_recommendations untuk ambil data profesi
            query = """
                SELECT 
                    s.user_id, 
                    s.id as session_id,
                    r.riasec_code_id,
                    codes.riasec_code,
                    rec.top_profession1_id,
                    rec.top_profession2_id
                FROM careerprofile_test_sessions s
                LEFT JOIN user_career_profiles ucp ON s.id = ucp.test_session_id
                JOIN riasec_results r ON s.id = r.test_session_id
                JOIN riasec_codes codes ON r.riasec_code_id = codes.id
                LEFT JOIN career_recommendations rec ON s.id = rec.test_session_id
                WHERE s.status = 'completed' 
                AND ucp.id IS NULL
            """
            cur.execute(query)
            missing_profiles = cur.fetchall()
            
            if missing_profiles:
                print(f"[!] Found {len(missing_profiles)} missing profiles. Processing...")
                for row in missing_profiles:
                    user_id, session_id, code_id, code_str, top1, top2 = row
                    
                    # Cek apakah user sudah punya profil aktif
                    cur.execute("SELECT id FROM user_career_profiles WHERE user_id = %s AND is_active = true", (user_id,))
                    if cur.fetchone():
                        is_active = False
                    else:
                        is_active = True
                    
                    # Insert manual
                    cur.execute("""
                        INSERT INTO user_career_profiles 
                        (user_id, test_session_id, top_profession1_id, top_profession2_id, riasec_code, is_active, created_at, activated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, now(), now())
                    """, (user_id, session_id, top1, top2, code_str, is_active))
                    print(f"[+] Created profile for user {user_id} (Session {session_id}, Active: {is_active})")
                
                conn.commit()
            
            cur.close()
            conn.close()
        except Exception as e:
            print(f"[!] Error in daemon: {e}")
            if conn: conn.close()
        
        # Cek setiap 5 detik
        time.sleep(5)

if __name__ == "__main__":
    run_daemon()

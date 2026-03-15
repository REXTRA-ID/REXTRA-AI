# force_insert.py
import psycopg2
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

def force_insert():
    db_url = os.getenv("DATABASE_URL")
    print(f"Connecting to: {db_url}")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    try:
        # 1. Cari user random
        cur.execute("SELECT id FROM users LIMIT 1")
        user_id = cur.fetchone()[0]
        
        # 2. Cari session random
        cur.execute("SELECT id FROM careerprofile_test_sessions LIMIT 1")
        session_id = cur.fetchone()[0]
        
        print(f"Mencoba insert manual untuk user {user_id} dan session {session_id}")
        
        # 3. Insert
        cur.execute("""
            INSERT INTO user_career_profiles 
            (user_id, test_session_id, top_profession1_id, top_profession2_id, riasec_code, is_active, created_at, activated_at)
            VALUES (%s, %s, 1, 2, 'RIA', true, now(), now())
        """, (user_id, session_id))
        
        conn.commit()
        print("INSERT BERHASIL DAN TER-COMMIT!")
        
        # 4. Cek langsung
        cur.execute("SELECT count(*) FROM user_career_profiles")
        print(f"Jumlah baris sekarang (di script ini): {cur.fetchone()[0]}")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    force_insert()

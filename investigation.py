# investigation.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def investigate():
    db_url = os.getenv("DATABASE_URL")
    print(f"Connecting to: {db_url}")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    try:
        # 1. Cek User Career Profiles
        cur.execute("SELECT count(*) FROM user_career_profiles")
        print(f"Total baris di user_career_profiles: {cur.fetchone()[0]}")
        
        # 2. Cek apakah ada data meski is_active False
        cur.execute("SELECT user_id, test_session_id, is_active FROM user_career_profiles")
        rows = cur.fetchall()
        print(f"Data di user_career_profiles: {rows}")

        # 3. Cek Sessions
        cur.execute("SELECT count(*) FROM careerprofile_test_sessions")
        print(f"Total baris di careerprofile_test_sessions: {cur.fetchone()[0]}")

        # 4. Cek Users
        cur.execute("SELECT count(*) FROM users")
        print(f"Total baris di users: {cur.fetchone()[0]}")

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    investigate()

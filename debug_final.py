# debug_final.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def debug():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    try:
        cur.execute("SELECT count(*) FROM users")
        print(f"Total Users: {cur.fetchone()[0]}")
        
        cur.execute("SELECT count(*) FROM careerprofile_test_sessions")
        print(f"Total Sessions: {cur.fetchone()[0]}")
        
        cur.execute("SELECT count(*) FROM user_career_profiles")
        print(f"Total Active Profiles: {cur.fetchone()[0]}")
        
        cur.execute("SELECT id, user_id, status FROM careerprofile_test_sessions ORDER BY id DESC LIMIT 1")
        last_session = cur.fetchone()
        print(f"Last Session: {last_session}")
        
        if last_session:
            cur.execute(f"SELECT count(*) FROM user_career_profiles WHERE test_session_id = {last_session[0]}")
            print(f"Profile exist for last session? {cur.fetchone()[0]}")

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    debug()

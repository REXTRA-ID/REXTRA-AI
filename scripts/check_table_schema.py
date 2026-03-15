# check_table_schema.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def check_schema():
    db_url = os.getenv("DATABASE_URL")
    print(f"Connecting to: {db_url}")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    try:
        cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'user_career_profiles'")
        rows = cur.fetchall()
        if not rows:
            print("Tabel 'user_career_profiles' TIDAK DITEMUKAN di information_schema.")
        else:
            print("KOLOM DI 'user_career_profiles':")
            for row in rows:
                print(f"  - {row[0]}: {row[1]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    check_schema()

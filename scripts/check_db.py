import psycopg2

DB_HOST = "103.171.84.248"
DB_PORT = 5433
DB_USER = "postgres"
DB_PASS = "password"
DB_NAME = "rextra"

conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, dbname=DB_NAME)
cur = conn.cursor()

print("=== profession_main_categories ===")
cur.execute("SELECT id, code, name FROM profession_main_categories ORDER BY id;")
rows = cur.fetchall()
if rows:
    for r in rows: print(f"  {r}")
else:
    print("  [KOSONG]")

print("\n=== profession_sub_categories ===")
cur.execute("SELECT id, code, name FROM profession_sub_categories ORDER BY id LIMIT 10;")
rows = cur.fetchall()
if rows:
    for r in rows: print(f"  {r}")
else:
    print("  [KOSONG]")

print("\n=== riasec_codes ===")
cur.execute("SELECT id, riasec_code FROM riasec_codes ORDER BY id;")
rows = cur.fetchall()
if rows:
    for r in rows: print(f"  {r}")
else:
    print("  [KOSONG]")

cur.close()
conn.close()
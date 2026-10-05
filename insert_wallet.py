import psycopg2
import uuid

conn = psycopg2.connect("postgresql://user:password@db:5432/features")
cur = conn.cursor()

cur.execute('''
INSERT INTO token_wallet (id, user_id, balance, updated_at) 
VALUES (%s, 'f24268ea-ade7-4d19-a090-f1a0c82b84c2', 100, NOW())
''', (str(uuid.uuid4()),))

conn.commit()
cur.close()
conn.close()
print("Wallet created!")

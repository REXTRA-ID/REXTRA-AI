import psycopg2

conn = psycopg2.connect("postgresql://user:password@db:5432/features")
cur = conn.cursor()

cur.execute('''
INSERT INTO users (id, fullname, email, password, phone_number, role, is_verified) 
VALUES ('f24268ea-ade7-4d19-a090-f1a0c82b84c2', 'Dian Anggraeni', 'studianggra@gmail.com', 'dummy', '0000', 'USER', true)
ON CONFLICT (id) DO NOTHING;
''')

conn.commit()
cur.close()
conn.close()
print("User inserted!")

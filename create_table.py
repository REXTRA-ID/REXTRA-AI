import psycopg2

conn = psycopg2.connect("postgresql://user:password@db:5432/features")
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS riasec_questions (
    id BIGSERIAL PRIMARY KEY,
    question_id VARCHAR(10) UNIQUE NOT NULL,
    riasec_type VARCHAR(1) NOT NULL,
    question_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
''')

conn.commit()
cur.close()
conn.close()
print("Table created!")

import psycopg2

conn = psycopg2.connect(dbname="mydatabase", user="postgres", password="7010@")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT,
        status VARCHAR(20) NOT NULL
    );
""")
conn.commit()

cursor.close()
conn.close()

print("Students table created successfully!")

import os, psycopg2

print("HOST:", os.getenv("POSTGRES_HOST"))
print("USER:", os.getenv("POSTGRES_USER"))
print("PASS:", os.getenv("POSTGRES_PASSWORD"))
print("DB:",   os.getenv("POSTGRES_DB"))

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
)
print("✅ Connected! Postgres version:", conn.server_version)
conn.close()

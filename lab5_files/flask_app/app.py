from flask import Flask
import redis
import psycopg2
import os

app = Flask(__name__)

# Redis setup
r = redis.Redis(host="redis", port=6379)

# PostgreSQL setup
POSTGRES_URL = os.getenv("POSTGRES_URL")
conn = psycopg2.connect(POSTGRES_URL)
cursor = conn.cursor()

@app.route("/")
def home():
    # Increment Redis counter
    count = r.incr("hits")

    # Example PostgreSQL query (fetch PostgreSQL version)
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    # Return the Redis count and PostgreSQL version
    return f"This page has been visited {count} times. Connected to PostgreSQL - version: {db_version}"

if __name__ == "__main__":
    app.run(host="0.0.0.0")

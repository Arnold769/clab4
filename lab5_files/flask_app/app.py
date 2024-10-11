from flask import Flask, jsonify
import os
import psycopg2
import redis

app = Flask(__name__)

# Redis setup
redis_host = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.StrictRedis.from_url(redis_host)

# PostgreSQL setup
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)

@app.route('/')
def home():
    return jsonify({
        "message": "Hello from Flask with Redis and PostgreSQL!"
    })

@app.route('/redis')
def redis_test():
    # Set a value in Redis
    redis_client.set('test_key', 'Redis connection successful!')
    value = redis_client.get('test_key')
    return jsonify({
        "message": value.decode("utf-8")
    })

@app.route('/postgres')
def postgres_test():
    # Test connection with PostgreSQL
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    return jsonify({
        "PostgreSQL Version": version
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

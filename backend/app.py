from flask import Flask, jsonify
import psycopg2
import redis
import os

app = Flask(__name__)

my_version = os.environ.get("VERSION", "1.0.0")

POSTGRES_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'postgres'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', ''),
    'host': os.getenv('POSTGRES_HOST', 'postgres'),
    'port': int(os.getenv('POSTGRES_PORT', 5432))
}

REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'redis'),
    'port': int(os.getenv('REDIS_PORT', 6379))
}

@app.route('/versions', methods=['GET'])
def get_versions():
    try:
        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(**POSTGRES_CONFIG)
        pg_cursor = pg_conn.cursor()
        pg_cursor.execute('SELECT version()')
        pg_version = pg_cursor.fetchone()[0]
        pg_cursor.close()
        pg_conn.close()
    except Exception as e:
        pg_version = f"Error connecting to PostgreSQL: {e}"

    try:
        # Connect to Redis
        redis_client = redis.Redis(**REDIS_CONFIG)
        redis_info = redis_client.info()
        redis_version = redis_info['redis_version']
    except Exception as e:
        redis_version = f"Error connecting to Redis: {e}"

    return jsonify({
        'backend': my_version,
        'postgres': pg_version,
        'redis': redis_version
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


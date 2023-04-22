import psycopg2
import time

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="central_116_database",
        user="postgres",
        password="postgres"
    )
    return conn

def store_data(snapshot_data):
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = 999
    snapshot = snapshot_data.decode()
    url = "http://example.com"
    origin = "example.com"
    
    cursor.execute(
        "INSERT INTO snapshots (datetime, snapshot, url, origin) VALUES (%s, %s, %s, %s)",
        (timestamp, snapshot, url, origin)
    )
    conn.commit()
    cursor.close()
    conn.close()
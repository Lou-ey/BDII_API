import psycopg2
import os

DB_NAME = os.getenv('dbname')
DB_USER = os.getenv('user')
DB_PASSWORD = os.getenv('password')
DB_HOST = os.getenv('host')
DB_PORT = os.getenv('port')

def db_conn():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print("Error connecting to database: ", e)
        return None

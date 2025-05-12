import psycopg2
import os
'''
def db_conn():
    DB_NAME = os.getenv('dbname')
    DB_USER = os.getenv('user')
    DB_PASSWORD = os.getenv('password')
    DB_HOST = os.getenv('host')
    DB_PORT = os.getenv('port')

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
'''

def db_conn_default():
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('USER')
    DB_PASSWORD = os.getenv('PASSWORD')
    DB_HOST = os.getenv('HOST')
    DB_PORT = os.getenv('PORT')

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


def db_conn(user_type):
    db_users = {
        "admin": {
            "user": os.getenv("ADMIN_USER"),
            "password": os.getenv("ADMIN_PASSWORD")
        },
        "rececionista": {
            "user": os.getenv("RECECIONISTA_USER"),
            "password": os.getenv("RECECIONISTA_PASSWORD")
        },
        "cliente": {
            "user": os.getenv("CLIENTE_USER"),
            "password": os.getenv("CLIENTE_PASSWORD")
        }
    }

    user = db_users[user_type]["user"]
    password = db_users[user_type]["password"]
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    dbname = os.getenv("DB_NAME")

    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return conn, None
    except Exception as e:
        return None, {
            "error": str(e),
            "user": user,
            "host": host,
            "dbname": dbname
        }
import psycopg2
import os

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


def db_conn_default():
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
def db_conn(user_type):
    # Mapeamento entre tipo de utilizador e variáveis de ambiente
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

    if user_type not in db_users:
        print("Tipo de utilizador inválido.")
        return None

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=db_users[user_type]["user"],
            password=db_users[user_type]["password"],
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar à base de dados como {user_type}: ", e)
        return None
'''
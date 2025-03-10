import psycopg2

def db_conn():
    try:
        conn = psycopg2.connect(
            dbname="db2022118542",
            user="a2022118542",
            password="a2022118542",
            host="aid.estgoh.ipc.pt",
            port="5432"
        )
        return conn
    except Exception as e:
        print("Erro ao conectar à base de dados:", e)
        return None

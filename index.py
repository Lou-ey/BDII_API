from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Função para conectar à base de dados
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

@app.route("/")
def hello():
    return jsonify({"message": "Hello, World!"})


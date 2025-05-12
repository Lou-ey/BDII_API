from flask import Flask, jsonify
from db.db import db_conn, db_conn_default
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt
from routes.utilizadores import utilizadores_routes
from routes.quartos import quarto_routes
from routes.img_quartos import img_quartos_routes
from routes.reservas import reservas_routes
from routes.login import login_routes
from routes.transacoes import trans_routes
import os
import psycopg2

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'ac7caF157DAB' # secret key para codificar os tokens JWT
app.config['JWT_TOKEN_LOCATION'] = ['headers'] # onde o token JWT será armazenado

jwt = JWTManager(app) # Inicia o JWTManager com a aplicação Flask

app.register_blueprint(utilizadores_routes)

app.register_blueprint(quarto_routes)

app.register_blueprint(img_quartos_routes)

app.register_blueprint(reservas_routes)

app.register_blueprint(login_routes)

app.register_blueprint(trans_routes)

@app.route('/')
def home():
    return "LUME!"

@app.route('/test_db', methods=['GET'])
def test_db():
    user_type = "admin"
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
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT current_user;")
            db_user = cur.fetchone()[0]
            cur.close()
            conn.close()
            return jsonify({
                "message": "Database connection successful!",
                "connected_user": db_user
            }), 200
    except Exception as e:
        return jsonify({
            "message": f"Erro ao conectar à base de dados: {str(e)}",
            "credenciais_usadas": {
                "user": user,
                "host": host,
                "dbname": dbname
            }
        }), 500






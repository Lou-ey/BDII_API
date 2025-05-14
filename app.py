from flask import Flask, jsonify
from db.db import db_conn, db_conn_default
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt
from routes.utilizadores import utilizadores_routes
from routes.quartos import quarto_routes
from routes.img_quartos import img_quartos_routes
from routes.reservas import reservas_routes
from routes.login import login_routes
from routes.transacoes import trans_routes

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
@jwt_required()
def test_db():
    claims = get_jwt()
    conn, error_info = db_conn(claims['tipo'])
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
    else:
        return jsonify({
            "message": "Erro ao conectar à base de dados.",
            "detalhes": error_info
        }), 500
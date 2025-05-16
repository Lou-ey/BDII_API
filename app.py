from flask import Flask, jsonify, render_template
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
    return render_template('home.html')
'''
@app.route('/test_db', methods=['GET'])
@jwt_required()
def test_db():
    claims = get_jwt()
    conn, error_info = db_conn(claims['tipo'])
    conn, error_info = db_conn_default() # Usar para conexão com a base de dados default apenas destinado para autenticação
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
        }), 500'''

@app.route('/test_db', methods=['GET'])
def test_db():
    # 1. Tenta conexão default
    conn = db_conn_default()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT current_user;")
        db_user = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({
            "message": "Conexão bem-sucedida com utilizador default.",
            "connected_user": db_user
        }), 200

    # 2. Se falhar, tenta com admin
    conn, error_info = db_conn("admin")
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT current_user;")
        db_user = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({
            "message": "Conexão default falhou. Conectado com sucesso como admin.",
            "connected_user": db_user
        }), 200

    # 3. Se falhar, tenta com rececionista
    conn, error_info = db_conn("rececionista")
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT current_user;")
        db_user = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({
            "message": "Conexão default e admin falharam. Conectado com sucesso como rececionista.",
            "connected_user": db_user
        }), 200

    # 4. Se tudo falhar
    return jsonify({
        "message": "Erro ao conectar à base de dados com qualquer utilizador.",
        "detalhes": error_info
    }), 500
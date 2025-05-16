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
    return """
    <html>
    <head>
        <title>API de Gestão de Hotel</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #2c3e50; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 8px 0; }
            a { text-decoration: none; color: #2980b9; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Bem-vindo à API de Gestão de Hotel</h1>
        <p>Abaixo encontra-se a lista de endpoints disponíveis:</p>
        <ul>
            <li><a href="/auth/login">/auth/login</a> – Login de utilizador</li>
            <li><a href="/user/get_all">/utilizadores</a> – Gestão de utilizadores (Admin)</li>
            <li><a href="/quartos/get_all">/quartos</a> – Consulta de quartos</li>
            <li><a href="/img_quartos/get_all/&lt;id_quarto&gt;">/img_quartos</a> – Imagens dos quartos</li>
            <li><a href="/reservas">/reservas</a> – Gestão de reservas</li>
            <li><a href="/transacoes">/transacoes</a> – Registo de pagamentos e reembolsos</li>
            <li><a href="/test_db">/test_db</a> – Testar conexão à base de dados</li>
        </ul>
        <p>Para aceder a endpoints protegidos, é necessário um token JWT.</p>
    </body>
    </html>
    """

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
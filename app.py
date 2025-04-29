from flask import Flask, jsonify
from db.db import db_conn
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from routes.utilizadores import utilizadores_routes
from routes.quartos import quarto_routes
from routes.img_quartos import img_quartos_routes
from routes.reservas import reservas_routes
from routes.login import login_routes
from routes.transacoes import trans_routes

app = Flask(__name__)

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
    try:
        current_user = get_jwt_identity()
        if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403
        conn = db_conn()
        return jsonify({"message": "Database connection successful!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error connecting to database: {str(e)}"}), 500




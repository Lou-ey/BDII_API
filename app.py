from flask import Flask, jsonify
from db.db import db_conn
from routes.quartos import quarto_routes
from routes.utilizadores import utilizadores_routes
from routes.quartos import quarto_routes
from routes.token import token_routes
import jwt
import datetime

app = Flask(__name__)


app.register_blueprint(utilizadores_routes, url_prefix='/user')

app.register_blueprint(quarto_routes, url_prefix='/quartos')

app.register_blueprint(token_routes)

@app.route('/')
def home():
    return "LUME!"

@app.route('/test_db')
def test_db():
    try:
        conn = db_conn()
        return jsonify({"message": "Database connection successful!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error connecting to database: {str(e)}"}), 500




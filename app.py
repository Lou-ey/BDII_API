from flask import Flask, jsonify
from db.db import db_conn
from routes.utilizadores import utilizadores_routes
from routes.quartos import quarto_routes
from routes.img_quartos import img_quartos_routes
import jwt
import datetime

app = Flask(__name__)

app.register_blueprint(utilizadores_routes)

app.register_blueprint(quarto_routes)

app.register_blueprint(img_quartos_routes)

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




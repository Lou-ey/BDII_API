from datetime import timedelta
from flask import Blueprint, jsonify, request
from db.db import db_conn
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/auth/login', methods=['GET', 'POST'])
@jwt_required()
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    conn = db_conn()
    if conn is None:
        return jsonify({"error": "Erro ao conectar à base de dados."}), 500

    cur = conn.cursor()
    cur.execute("SELECT * FROM utilizadores WHERE email = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        access_token = create_access_token(identity={
            "id_utilizador": user[0],
            "email": user[2],
            "tipo": user[7]
        }, expires_delta=timedelta(hours=1))
        return jsonify({"access_token": access_token, "user": user[1], "tipo": user[7], "id_utilizador": user[0]}), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401
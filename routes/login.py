from flask import request, jsonify, Blueprint
from db.db import db_conn
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/auth/login', methods=['POST'])
@jwt_required()
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    conn = db_conn()
    if conn is None:
        return jsonify({"error": "Erro ao conectar à base de dados."}), 500

    cur = conn.cursor()
    cur.execute("SELECT * FROM utilizadores WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        access_token = create_access_token(identity={"username": username})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401
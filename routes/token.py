import os
import datetime
from os import access

import jwt
from flask import Flask, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.db import db_conn

token_routes = Blueprint('token_routes', __name__)

secret = os.getenv('secret')

@token_routes.route('/token')
@jwt_required()
def token():
    try:
        # Get the current user from the JWT token
        current_user = get_jwt_identity()
        if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@token_routes.route('/decode_token')
def decode_token(tokken):
    data = jwt.JWT.decode(tokken, secret)
    return jsonify({"data": data})
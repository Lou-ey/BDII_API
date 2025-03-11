import os
import datetime
import jwt
from flask import Flask, jsonify, Blueprint

token_routes = Blueprint('token_routes', __name__)

secret = os.getenv('secret')

@token_routes.route('/token')
def token():
    tokken = jwt.JWT.encode(
        payload={"user_id": 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
        key=secret,
        alg="HS256",
    )
    return jsonify({"token": tokken})

@token_routes.route('/decode_token')
def decode_token(tokken):
    data = jwt.JWT.decode(tokken, secret)
    return jsonify({"data": data})
import os
import datetime
import jwt
from flask import Flask, jsonify, Blueprint

token_routes = Blueprint('token_routes', __name__)

secret = os.getenv('secret')

@token_routes.route('/token')
def token():
    token = jwt.JWT.encode(
        payload={"user_id": 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
        key=secret,
        alg="HS256",
    )
    return jsonify({"token": token})

@token_routes.route('/decode_token')
def decode_token(token):
    token = jwt.JWT.decode(
        token=token,
        key=secret,
        alg="HS256",
    )
    return jsonify({"decoded_token": token})
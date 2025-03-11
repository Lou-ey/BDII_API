from flask import Flask, jsonify
from db.db import db_conn
from routes.routes import test_db

app = Flask(__name__)


@app.route('/')
def home():
    return "LUME!"


app.register_blueprint(test_db)












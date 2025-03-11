from flask import Flask, jsonify
from db.db import db_conn
from routes.routes import *

app = Flask(__name__)

app.register_blueprint(employee_routes)
app.register_blueprint(test_db)

@app.route('/')
def home():
    return "LUME!"





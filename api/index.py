from flask import Flask, jsonify
from db.db import db_conn

app = Flask(__name__)

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





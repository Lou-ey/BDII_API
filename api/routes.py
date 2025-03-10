from flask import Blueprint, jsonify, request
from db import db_conn

employee_routes = Blueprint('employee_routes', __name__)

@employee_routes.route('/emp', methods=['GET'])
def get_employee():
    conn = db_conn()
    if not conn:
        return jsonify({"error": "Erro de conexão à base de dados"}), 500
    cur = conn.cursor()
    cur.execute("SELECT * FROM emp")
    result = cur.fetchall()
    conn.close()
    return jsonify(result)

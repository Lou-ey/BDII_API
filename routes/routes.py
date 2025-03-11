from flask import Blueprint, jsonify
from db.db import db_conn

employee_routes = Blueprint('employee_routes', __name__)
test_db = Blueprint('test_db', __name__)

@employee_routes.route('/emp', methods=['GET'])
def get_employee():
    try :
        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM employee")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"employees": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@test_db.route('/test_db')
def test_db():
    try:
        conn = db_conn()
        return jsonify({"message": "Database connection successful!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error connecting to database: {str(e)}"}), 500
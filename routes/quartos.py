from flask import Blueprint, jsonify
from db.db import db_conn

quarto_routes = Blueprint('quarto_routes', __name__)

@quarto_routes.route('/quartos/get_all')
def get_quartos():
    try :
        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM quartos")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"Row": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
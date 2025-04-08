from flask import Blueprint, jsonify, request
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

@quarto_routes.route('/quartos/<int:id_quarto>')
def get_quartos_by_id(id_quarto):
    try:
        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM quartos WHERE id_quarto = %s", (id_quarto,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return jsonify({"row": row})
        else:
            return jsonify({"error": "Quarto não encontrado."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

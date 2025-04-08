from flask import Blueprint, jsonify, request
from db.db import db_conn

img_quartos_routes = Blueprint('img_quartos_routes', __name__)

@img_quartos_routes.route('/img_quartos/get_all/<int:id_quarto>', methods=['GET'])
def get_img_quartos(id_quarto):
    try:
        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT id_img, encode(img, 'base64') AS img_base64, quarto_id_quarto FROM img_quartos WHERE quartos_id_quarto = %s", (id_quarto,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"Row": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
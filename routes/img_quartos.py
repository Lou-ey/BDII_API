from flask import Blueprint, jsonify, request
from db.db import db_conn
from flask_jwt_extended import jwt_required, get_jwt_identity

img_quartos_routes = Blueprint('img_quartos_routes', __name__)

@img_quartos_routes.route('/img_quartos/get_all/<int:id_quarto>', methods=['GET'])
@jwt_required()
def get_img_quartos(id_quarto):
    try:
        current_user = get_jwt_identity()
        if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403
        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT id_img, encode(img, 'base64') AS img_base64 FROM img_quartos WHERE quartos_id_quarto = %s", (id_quarto,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"Row": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@img_
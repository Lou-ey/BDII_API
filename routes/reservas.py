from flask import Blueprint, jsonify, request
from db.db import db_conn
from flask_jwt_extended import jwt_required, get_jwt_identity

reservas_routes = Blueprint('reservas_routes', __name__)

@reservas_routes.route('/reservas/get_all', methods=['GET'])
@jwt_required()
def get_all_reservas():
    try:
        current_user = get_jwt_identity()
        if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403

        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM reservas_view")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"Row": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservas_routes.route('/reservas/<int:id_reserva>', methods=['GET'])
@jwt_required()
def get_reserva_by_id(id_reserva):
    try:
        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM reservas_view WHERE id_reserva = %s", (id_reserva,))
        rows = cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({"Row": rows})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservas_routes.route('/reservas/insert', methods=['POST'])
def insert_reserva():
    try:
        data = request.get_json()

        ckeck_in = data.get('ckeck_in')
        ckeck_out = data.get('ckeck_out')
        pessoas = data.get('pessoas')
        cancelado = data.get('cancelado')
        met_pagamento = data.get('met_pagamento')
        id_cliente = data.get('id_cliente')
        id_quarto = data.get('id_quarto')

        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("CALL insert_reservation(%s, %s, %s, %s, %s, %s, %s)",
                    (ckeck_in, ckeck_out, pessoas, cancelado, met_pagamento, id_cliente, id_quarto))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Reserva inserida com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
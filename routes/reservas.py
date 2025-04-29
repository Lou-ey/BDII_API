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

@reservas_routes.route('/reservas/<int:id_reserva>/cancel', methods=['PUT'])
@jwt_required()
def cancel_reservation(id_reserva):
    try:
        current_user = get_jwt_identity()
        db = db_conn()
        if db is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500
        cur = db.cursor()
        cur.execute("SELECT utilizadores_id_cliente FROM reservas_view WHERE id_reserva = %s", (id_reserva,))
        user_id = cur.fetchone()

        if user_id is None:
            return jsonify({"error": "Reserva não encontrada."}), 404

        if current_user != user_id[0]:
            return jsonify({"error": "Acesso negado."}), 403

        cur.execute("CALL cancel_reservation(%s)", (id_reserva,))
        db.commit()
        cur.close()
        db.close()
        return jsonify({"message": "Reserva cancelada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
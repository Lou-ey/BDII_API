from flask import Blueprint, jsonify, request
from db.db import db_conn
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

reservas_routes = Blueprint('reservas_routes', __name__)

@reservas_routes.route('/reservas/get_all', methods=['GET'])
@jwt_required()
def get_all_reservas():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims['tipo'] != 'admin' and claims['tipo'] != 'rececionista':
            return jsonify({"error": "Acesso negado."}), 403

        conn = db_conn()
        #conn = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
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
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims['tipo'] != 'admin' and claims['tipo'] != 'rececionista':
            return jsonify({"error": f"Acesso negado. Com o tipo {claims['tipo']} "}), 403
        conn = db_conn()
        #conn = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
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
@jwt_required()
def insert_reserva():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims['tipo'] != 'rececionista' and claims['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403
        data = request.get_json()

        check_in = data.get('check_in')
        check_out = data.get('check_out')
        pessoas = data.get('pessoas')
        #cancelado = data.get('cancelado') Quando é criado o valor default é falso
        #met_pagamento = data.get('met_pagamento') Quando é criado o valor default é falso
        id_cliente = data.get('id_cliente')
        id_quarto = data.get('id_quarto')

        conn = db_conn()
        #conn = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("CALL insert_reservation(%s, %s, %s, %s, %s)",
                    (check_in, check_out, pessoas, id_cliente, id_quarto))
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
        claims = get_jwt()
        if claims['tipo'] != 'admin' and claims['tipo'] != 'rececionista':
            return jsonify({"error": "Acesso negado."}), 403
        db = db_conn()
        #db = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd de forma dinamica dependendo do tipo de utilizador
        if db is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500
        cur = db.cursor()
        cur.execute("SELECT utilizadores_id_cliente FROM reservas_view WHERE id_reserva = %s", (id_reserva,))
        user_id = cur.fetchone()

        if user_id is None:
            return jsonify({"error": "Reserva não encontrada."}), 404

        #if current_user != user_id[0]:  #só a pessoa da reserva pode cancelar
         #   return jsonify({"error": "Acesso negado."}), 403

        cur.execute("CALL cancel_reservation(%s)", (id_reserva,))
        db.commit()
        cur.close()
        db.close()
        return jsonify({"message": "Reserva cancelada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservas_routes.route('/reservas/reserva_by_year', methods=['GET'])
@jwt_required()
def get_reserva_by_year():
    try:
        claims = get_jwt()
        if claims["tipo"] != "admin":
            return jsonify({"error": "Acesso negado."}), 403

        ano = request.args.get('ano', default=None, type=int) # Obtem o ano do url atraves do ?ano=2024
        if not ano:
            return jsonify({"error": "Parâmetro 'ano' em falta."}), 400

        data_inicio = f"{ano}-01-01"
        data_fim = f"{ano + 1}-01-01"

        conn = db_conn()
        #conn = db_conn(claims['tipo']) # Usar esta conexão para conexao ha bd dinamica dependendo do tipo de utilizador
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM reservas 
            WHERE checkin >= %s AND checkin < %s
        """, (data_inicio, data_fim))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"Row": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@reservas_routes.route('/reservas/get_active_reservations', methods=['GET'])
@jwt_required()
def get_active_reservations():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()

        conn = db_conn()
        #conn = db_conn(claims['tipo']) # Usar esta conexão para conexao ha bd dinamica dependendo do tipo de utilizador
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        if claims["tipo"] == "admin" or claims["tipo"] == "rececionista":
            cur = conn.cursor()
            cur.execute("CALL get_active_reservations()")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify({"Row": rows})
        elif claims["tipo"] == "cliente":
            cur = conn.cursor()
            cur.execute("CALL get_active_reservations(%s)", (current_user,))
            rows = cur.fetchall()
            cur.close()
            conn.close()
            if not rows:
                return jsonify({"error": "Nenhuma reserva ativa encontrada."}), 404
            else:
                return jsonify({"Row": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
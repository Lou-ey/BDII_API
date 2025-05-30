from flask import Blueprint, jsonify, request
from db.db import db_conn
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

trans_routes = Blueprint('trans_routes', __name__)

@trans_routes.route('/reservas/<int:id_reserva>/pagar', methods=['POST'])
@jwt_required()
def pay(id_reserva):
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims['tipo'] != 'cliente':
            return jsonify({"error": "Acesso negado."}), 403

        data = request.get_json()
        met_pagamento = data.get('met_pagamento')

        #db = db_conn()
        conn, _ = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT utilizadores_id_cliente FROM reservas_view WHERE id_reserva = %s", (id_reserva,))
        user_id = cur.fetchone()[0]
        current_user = int(current_user) # Converter para inteiro
        if current_user != user_id:
            return jsonify({"debug": f"{type(current_user)} {type(user_id)}"}), 500
            #return jsonify({"error": f"Acesso negado. Com o id: {current_user} e o id da reserva e: {user_id}"}), 403

        cur.execute("CALL pay_reserva(%s, %s)", (id_reserva, met_pagamento))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Reserva paga com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trans_routes.route('/transacoes/get_all', methods=['GET'])
@jwt_required()
def get_all_transacoes():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims['tipo'] != 'admin':
            #if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403

        #conn = db_conn()
        conn = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM transacoes")
        col_names = [desc[0] for desc in cur.description]  # Obter nomes das colunas
        rows = cur.fetchall()

        result = []
        for row in rows:  # Combinar nomes das colunas com valores das linhas
            row_dict = dict(zip(col_names, row))
            result.append(row_dict)
        cur.close()
        conn.close()
        return jsonify({"Row": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trans_routes.route('/transacoes/<int:id_reserva>', methods=['GET'])
@jwt_required()
def get_transacoes(id_reserva):
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims['tipo'] != 'admin':
            #if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403

        #conn = db_conn()
        conn, _ = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM transacoes_view WHERE id_reserva = %s", (id_reserva,))
        col_names = [desc[0] for desc in cur.description]  # Obter nomes das colunas
        rows = cur.fetchall()

        result = []
        for row in rows:  # Combinar nomes das colunas com valores das linhas
            row_dict = dict(zip(col_names, row))
            result.append(row_dict)

        cur.close()
        conn.close()
        return jsonify({"Row": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import Blueprint, jsonify, request
from db.db import db_conn
from flask_jwt_extended import jwt_required, get_jwt_identity

quarto_routes = Blueprint('quarto_routes', __name__)

@quarto_routes.route('/quartos/get_all')
@jwt_required()
def get_quartos():
    try :
        current_user = get_jwt_identity()
        if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403
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

@quarto_routes.route('/quartos/update/<int:id_quarto>', methods=['PUT'])
@jwt_required()
def update_quarto(id_quarto):
    try:
        current_user = get_jwt_identity()
        if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403

        data = request.get_json()

        parametro_a_alterar = data['parametro_a_alterar']
        novo_valor = data['novo_valor']

        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500
        cur = conn.cursor()
        cur.execute("CALL update_room(%s, %s, %s)", (id_quarto, parametro_a_alterar, novo_valor))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Quarto atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quarto_routes.route('/quartos/insert', methods=['POST'])
@jwt_required()
def insert_quarto():
    try:
        current_user = get_jwt_identity()
        if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403
        data = request.get_json()

        numero = data['numero']
        disponibilidade = data['disponibilidade']
        capacidade = data['capacidade']
        image = data['image']
        preco = data['preco']

        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("CALL insert_room(%s, %s, %s, %s, %s)",
                    (numero, disponibilidade, capacidade, image, preco))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Quarto inserido com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quarto_routes.route('/quartos/check_disponibilidade', methods=['GET'])
def check_disponibilidade():
    try:
        data = request.get_json()

        ckeck_in = data['ckeck_in']
        ckeck_out = data['ckeck_out']
        id_quarto = data['id_quarto']

        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT check_disponibilidade(%s, %s, %s)", (ckeck_in, ckeck_out, id_quarto))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return jsonify({"row": row})
        else:
            return jsonify({"error": "Quarto não encontrado."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

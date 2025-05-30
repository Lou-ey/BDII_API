from flask import Blueprint, jsonify, request
from db.db import db_conn, db_conn_default
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

quarto_routes = Blueprint('quarto_routes', __name__)

@quarto_routes.route('/quartos/get_all')
@jwt_required()
def get_quartos():
    try :
        current_user = get_jwt_identity()
        claims = get_jwt()
        #if claims['tipo'] != 'admin' and claims['tipo'] != 'rececionista':
        if claims['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403
        #conn = db_conn()
        conn, _ = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM quartos")
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

@quarto_routes.route('/quartos/<int:id_quarto>')
@jwt_required()
def get_quartos_by_id(id_quarto):
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims['tipo'] != 'admin' and claims['tipo'] != 'rececionista':
            #if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403

        #conn = db_conn()
        conn, _ = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM quartos WHERE id_quarto = %s", (id_quarto,))
        col_names = [desc[0] for desc in cur.description]  # Obter nomes das colunas
        rows = cur.fetchall()

        result = []
        for row in rows:  # Combinar nomes das colunas com valores das linhas
            row_dict = dict(zip(col_names, row))
            result.append(row_dict)
        cur.close()
        conn.close()

        if rows:
            return jsonify({"Row": result}), 200
        else:
            return jsonify({"error": "Quarto não encontrado."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quarto_routes.route('/quartos/update/<int:id_quarto>', methods=['PUT'])
@jwt_required()
def update_quarto(id_quarto):
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403

        data = request.get_json()

        parametro_a_alterar = data['parametro_a_alterar']
        novo_valor = data['novo_valor']

        #conn = db_conn()
        conn, _ = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
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
        claims = get_jwt()
        if claims['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403

        data = request.get_json()

        numero = data['numero']
        disponibilidade = data['disponibilidade']
        capacidade = data['capacidade']
        #image = data['image']
        preco = data['preco']

        #conn = db_conn()
        conn, _ = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("CALL insert_room(%s, %s, %s, %s)",
                    (numero, disponibilidade, capacidade, preco))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Quarto inserido com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quarto_routes.route('/quartos/check_disponibilidade/<int:id_quarto>', methods=['POST'])
def check_disponibilidade(id_quarto):
    try:
        data = request.get_json()

        ckeck_in = data['ckeck_in']
        ckeck_out = data['ckeck_out']
        #id_quarto = data['id_quarto']

        conn, _ = db_conn_default()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT check_disponibilidade(%s, %s, %s)", (ckeck_in, ckeck_out, id_quarto))
        col_names = [desc[0] for desc in cur.description]  # Obter nomes das colunas
        rows = cur.fetchall()

        result = []
        for row in rows:  # Combinar nomes das colunas com valores das linhas
            row_dict = dict(zip(col_names, row))
            result.append(row_dict)
        cur.close()
        conn.close()

        if row:
            return jsonify({"row": result}), 200
        else:
            return jsonify({"error": "Quarto não encontrado."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

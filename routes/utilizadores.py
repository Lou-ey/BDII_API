from flask import Blueprint, jsonify, request
from db.db import db_conn, db_conn_default
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

utilizadores_routes = Blueprint('utilizadores_routes', __name__)

@utilizadores_routes.route('/user/get_all', methods=['GET'])
@jwt_required()
def get_all_users():
    try :
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
        cur.execute("SELECT * FROM users_view")
        col_names = [desc[0] for desc in cur.description] # Obter nomes das colunas
        rows = cur.fetchall()

        result=[]
        for row in rows: # Combinar nomes das colunas com valores das linhas
            row_dict = dict(zip(col_names, row))
            result.append(row_dict)

        cur.close()
        conn.close()

        return jsonify({"Row": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@utilizadores_routes.route('/user/<int:id_utilizador>', methods=['GET'])
@jwt_required()
def get_user_by_id(id_utilizador):
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims['tipo'] != 'admin':
            #if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403

        #conn = db_conn_default()
        # usa-se o "_" para ignorar o segundo valor retornado pela função db_conn
        conn, _ = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()

        cur.execute("SELECT * FROM users_view WHERE id_utilizador = %s", #chamar o procedimento
                    (id_utilizador,)) #levar os valores
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

'''
@utilizadores_routes.route('/auth/register', methods=['POST'])
def insert_user():
    try:

        data = request.get_json()  #ir buscar o body ao request http

        nome = data.get('nome')  #extrair variaveis
        email = data.get('email')
        password = data.get('password')
        nif = data.get('nif')
        telefone = data.get('telefone')
        idade = data.get('idade')
        tipo = data.get('tipo')

        conn = db_conn_default()
        #conn = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador

        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()

        cur.execute("CALL insert_user(%s, %s, %s, %s, %s, %s, %s)", #chamar o procedimento
                    (nome, email, password, nif, telefone, idade, tipo)) #levar os valores


        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Utilizador inserido com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
'''

@utilizadores_routes.route('/auth/register', methods=['POST'])
def public_register_cliente():
    try:
        data = request.get_json()

        #if data.get('tipo') != 'cliente':
            #return jsonify({"error": "Só é permitido criar contas do tipo cliente neste endpoint."}), 403

        nome = data.get('nome')
        email = data.get('email')
        password = data.get('password')
        nif = data.get('nif')
        telefone = data.get('telefone')
        idade = data.get('idade')

        conn, _ = db_conn_default()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("CALL insert_user(%s, %s, %s, %s, %s, %s, %s)",
                    (nome, email, password, nif, telefone, idade, 'cliente'))  # Força tipo cliente
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Conta cliente criada com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@utilizadores_routes.route('/auth/register/staff', methods=['POST'])
@jwt_required()
def register_staff():
    try:
        claims = get_jwt()

        if claims['tipo'] != 'admin':
            return jsonify({"error": "Apenas administradores podem criar contas de staff."}), 403

        data = request.get_json()
        tipo = data.get('tipo')

        if tipo not in ['admin', 'rececionista']:
            return jsonify({"error": "Só pode registar utilizadores do tipo admin ou rececionista."}), 400

        nome = data.get('nome')
        email = data.get('email')
        password = data.get('password')
        nif = data.get('nif')
        telefone = data.get('telefone')
        idade = data.get('idade')

        conn, _ = db_conn(claims['tipo'])
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("CALL insert_user(%s, %s, %s, %s, %s, %s, %s)",
                    (nome, email, password, nif, telefone, idade, tipo))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": f"Conta {tipo} criada com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

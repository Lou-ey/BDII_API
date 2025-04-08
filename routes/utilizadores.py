from flask import Blueprint, jsonify, request
from db.db import db_conn

utilizadores_routes = Blueprint('utilizadores_routes', __name__)

@utilizadores_routes.route('/user/get_all', methods=['GET'])
def get_all_users():
    try :
        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT * FROM users_view")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"Row": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@utilizadores_routes.route('/user/<int:id_utilizador>', methods=['GET'])
def get_user_by_id(id_utilizador):
    try:
        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()

        cur.execute("SELECT * FROM users_view WHERE id_utilizador = %s", #chamar o procedimento
                    (id_utilizador,)) #levar os valores
        rows = cur.fetchone()

        cur.close()
        conn.close()

        return jsonify({"Row": rows})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@utilizadores_routes.route('/user/insert', methods=['POST'])
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

        conn = db_conn()
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
        return jsonify({"Erro ao inserir Utilizador, error": str(e)}), 500



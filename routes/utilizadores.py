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


@utilizadores_routes.route('/user/insert', methods=['POST'])
def insert_user():
    try:
        data = request.get_json()

        nome = data.get('nome')
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
        cur.callproc('insert_user', (nome, email, password, nif, telefone, idade, tipo))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Utilizador inserido com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



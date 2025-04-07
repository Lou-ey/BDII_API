from flask import Blueprint, jsonify
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


    """ 
@utilizadores_routes.route('/user/get_by_id', methods=['GET'])
def get_user_by_id():
    try :
        conn = db_conn()
        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500
            

"""
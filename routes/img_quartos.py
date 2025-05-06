from flask import Blueprint, jsonify, request
from db.db import db_conn
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

img_quartos_routes = Blueprint('img_quartos_routes', __name__)

#ir buscar todas as imagens de um quarto (qualquer pessoa pode ver as imagens)
@img_quartos_routes.route('/img_quartos/get_all/<int:id_quarto>', methods=['GET'])
#@jwt_required()
def get_img_quartos(id_quarto):
    try:
        #current_user = get_jwt_identity()
        #claims = get_jwt()
       # if claims['tipo'] != 'admin':
            #if current_user['tipo'] != 'admin':
          #  return jsonify({"error": "Acesso negado."}), 403

        conn = db_conn()
        #conn = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador

        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        cur.execute("SELECT id_img, encode(img, 'base64') AS img_base64 FROM img_quartos WHERE quartos_id_quarto = %s", (id_quarto,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if not rows:
            return jsonify({"error": "Nenhuma imagem encontrada para este quarto."}), 404
        else:
            return jsonify({"rows": rows}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# inserir imagem
@img_quartos_routes.route('/img_quartos/insert/<int:id_quarto>', methods=['POST'])
@jwt_required()
def insert_img_quarto(id_quarto):
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()
        if claims['tipo'] != 'admin':
            #if current_user['tipo'] != 'admin':
            return jsonify({"error": "Acesso negado."}), 403

        conn = db_conn()
        #conn = db_conn(claims['tipo']) # Usar esta conexão para conexao a bd dinamica dependendo do tipo de utilizador

        if conn is None:
            return jsonify({"error": "Erro ao conectar à base de dados."}), 500

        cur = conn.cursor()
        data = request.get_json()
        img_base64 = data.get('img_base64')

        if not img_base64:
            return jsonify({"error": "Imagem não fornecida."}), 400

        #img = bytes(img_base64, 'utf-8')
        cur.execute("CALL insert_room_img(%s, %s)", (id_quarto, img_base64))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Imagem inserida com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
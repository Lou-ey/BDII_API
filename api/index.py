from flask import Flask, jsonify
from db import db_conn
from routes import employee_routes

app = Flask(__name__)

# Registar rotas do ficheiro routes.py
app.register_blueprint(employee_routes)

@app.route('/')
def home():
    return jsonify({"message": "API Flask na Vercel está a funcionar!"})

if __name__ == '__main__':
    app.run()



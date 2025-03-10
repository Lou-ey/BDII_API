from flask import Flask, jsonify
from db import db_conn
from routes import employee_routes

app = Flask(__name__)

app.register_blueprint(employee_routes)

@app.route('/')
def home():
    return

if __name__ == '__main__':
    app.run()



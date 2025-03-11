from flask import Flask, jsonify
from routes import employee_routes

app = Flask(__name__)

app.register_blueprint(employee_routes)

@app.route('/')
def home():
    return jsonify({"message": "API Flask na Vercel está a funcionar!"})

if __name__ == '__main__':
    app.run()


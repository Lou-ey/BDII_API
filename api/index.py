from flask import Flask, jsonify
from routes import employee_routes

app = Flask(__name__)

#app.register_blueprint(employee_routes)

@app.route('/')
def home():
    return jsonify({"message": "Hello, Vercel!"})

# Vercel precisa desta variável para encontrar a app
if __name__ == "__main__":
    app.run()




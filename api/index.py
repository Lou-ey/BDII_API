from flask import Flask
from routes import employee_routes

app = Flask(__name__)

app.register_blueprint(employee_routes)

@app.route('/')
def home():
    return "LUME!"



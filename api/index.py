from flask import Flask, jsonify
from routes import employee_routes

app = Flask(__name__)

#app.register_blueprint(employee_routes)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'



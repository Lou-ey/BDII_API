from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "API Flask na Vercel está a funcionar!"

@app.route('/about')
def about():
    return 'About'



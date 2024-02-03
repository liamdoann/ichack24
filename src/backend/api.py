from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Home"

@app.route('/auth/login', methods=['GET'])
def login():
    return {'message': 'Login'}

@app.route('/auth/register', methods=['POST', 'GET'])
def register():
    pass

@app.route('/logout', methods=['POST'])
def logout():
    pass



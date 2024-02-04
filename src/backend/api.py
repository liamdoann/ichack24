from flask import Flask, request, jsonify
from backend import *
import sys

app = Flask(__name__)

@app.route('/validate-login', methods=['POST'])
def validate_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    classes, school = retrieveTeacher(username, password)
    
    if school:
        return jsonify({'success': True, 'classes': classes, 'school': school})
    else:
        return jsonify({'success': False})

@app.route('/get-classes', methods=['GET'])
def get_classes():
    args = request.args
    usr = args['username']
    pwd = args['password']
    print(usr, file=sys.stdout)
    print(pwd, file=sys.stdout)
    classes, school = retrieveTeacher(usr, pwd)
    print(classes, file=sys.stdout)
    print(school, file=sys.stdout)
    return jsonify(classes=classes, school=school)

@app.route('/get-students', methods=['GET'])
def get_students():
    args = request.args
    pass

@app.route('/auth/login', methods=['GET'])
def login():
    return {'message': 'Login'}

@app.route('/auth/register', methods=['POST', 'GET'])
def register():
    pass

@app.route('/logout', methods=['POST'])
def logout():
    pass
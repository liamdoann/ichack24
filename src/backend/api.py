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

@app.route('/get-students', methods=['POST'])
def get_students():
    data = request.get_json()
    className = data.get('class')
    school = data.get('school')
    students = getStudents(className, school)

    return jsonify({'students': [{'Name': name} for name in students]})
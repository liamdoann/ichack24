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

@app.route('/find-student', methods=['POST'])
def find_student():
    data = request.get_json()
    studentName = data.get('student')
    className = data.get('class')
    school = data.get('school')
    lastImprovements, percentages, average, avgDelta, positiveOrder, negativeOrder, improvementOrder = getStudentInfo(studentName, className, school)
    return jsonify({'lastImprovements': lastImprovements, 'percentages': percentages, 'average': average, 'avgDelta': avgDelta, 'positiveOrder': positiveOrder, 'negativeOrder': negativeOrder, 'improvementOrder': improvementOrder})

@app.route('/submit-report', methods=['POST'])
def submit_report():
    data = request.get_json()
    studentName = data.get('student')
    className = data.get('class')
    school = data.get('school')
    score = data.get('score')
    positiveComments = data.get('positive')
    negativeComments = data.get('negative')
    improvementComments = data.get('improvement')
    report = addReport(studentName, className, score, school, positiveComments, negativeComments, improvementComments)
    return jsonify({'report': report})
import sqlite3
import openai
from flask import Flask, jsonify

api_file = open("api-key", "r")
api_key = api_file.readline()
api_key.strip()
api_file.close()

# Create a connection to the database
def connect(dbID):
    conn = sqlite3.connect(dbID + '.db')
    return conn


# Reetrieve user credentials from the webpage - this is some flask shit idk someone else can do that
def retrieveCredentials(request):
    username = request.form['username']
    password = request.form['password']
    return username, password

# Check if the user exists in the database
def checkUserExists(username, password, conn):
    cursor = conn.cursor()
    cursor.execute(f"SELECT school FROM teachers WHERE username = '{username}' AND password = '{password}'")
    school = cursor.fetchone()
    return school

# Send the classes to the webpage
def sendClasses(classes, school):
    # TODO()
    pass

# Send an error to the webpage if the credentials are incorrect
def credentialError():
    # TODO()
    pass

def retrieveTeacher(username, password):
    print(f"Requesting teacher: {username} with password: {password}")
    conn = connect('allTeachers')
    print(username, password)
    school = checkUserExists(username, password, conn)
    print(school)
    if school is None:
        print("Credential error")
        conn.close()
        return None, False
    school = school[0]
    conn.close()
    conn = connect(school)
    print("Connected to school database")
    cursor = conn.cursor()
    cursor.execute(f"SELECT tid FROM teachers WHERE name = '{username}'")
    tid = cursor.fetchone()[0]
    print(f"Teacher ID: {tid}")
    cursor.execute(f"SELECT name FROM classes WHERE tid = {tid}")
    results = cursor.fetchall()
    newResults = [result[0] for result in results]
    print("Classes: \n", newResults)
    conn.close()
    return newResults, school    # Send the classes to the webpage

# Retrieve the students in a class since the last report
def getStudentAverage(school, studentId, classId):
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"SELECT date FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC LIMIT 1")
    if cursor.fetchone() is None:
        cursor.execute(f"SELECT * FROM marks WHERE sid = {studentId} AND cid = {classId}")
    else:
        cursor.execute(f"""SELECT * FROM marks WHERE sid = {studentId} AND cid = {classId} AND date > 
                            (SELECT date FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC LIMIT 1)""")
    marks = cursor.fetchall()
    total = 0
    for mark in marks:
        total += mark[3] / mark[4]
    if len(marks) == 0:
        average = 0
    else:
        average = int(total / len(marks))
    conn.close()
    return average

reportCategories = {
    "engagement": ["The student has been engaged in class discussions", "The student has lacked engagement in class discussions", "the student has improved their engagement in class discussions"],
    "participation": ["The student has participated in class activities", "The student has not participated in class activities", "The student has improved their participation in class activities"],
    "homework": ["The student has completed all homework assignments", "The student has not completed all homework assignments", "The student has improved their completion of homework assignments"],
    "attitude": ["The student has had a positive attitude in class", "The student has had a negative attitude in class", "The student has improved their attitude in class"],
    "respect": ["The student has shown respect to their peers and teachers", "The student has not shown respect to their peers and teachers", "The student has improved their respect to their peers and teachers"],
    "attendance": ["The student has had good attendance", "The student has had poor attendance", "The student has improved their attendance"],
    "punctuality": ["The student has been punctual", "The student has been late to class", "The student has improved their punctuality"],
    "organisation": ["The student has been organised", "The student has been disorganised", "The student has improved their organisation"],
    "effort": ["The student has put in a lot of effort", "The student has not put in a lot of effort", "The student has improved their effort"],
    "behaviour": ["The student has had good behaviour", "The student has had poor behaviour", "The student has improved their behaviour"],
    "performance": ["The student has performed well in class", "The student has not performed well in class", "The student has improved their performance in class"]
}

def getClassId(school, className):
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"SELECT cid FROM classes WHERE name = '{className}'")
    classId = cursor.fetchone()[0]
    conn.close()
    return classId

def generate_scores(category, reports):
    score = 0
    i = 5
    improvements = []
    for report in reports:
        if reportCategories[category][0] in reports[report]:
            score += max(i, 0) ** 2
        if reportCategories[category][1] in reports[report]:
            score -= max(i, 0) ** 2
        if reportCategories[category][2] in reports[report]:
            score += max(i, 0) ** 1.5
            if i == 5:
                improvements.append(category)
        i += 1
    return int(score), improvements

# Retrieve information about a given student in a class. Returns:
# - A list of what the student was told to improve on in the last report
# - A list of percentages of marks the student has received in the class since the last report
# - The average percentage of marks the student has received since the last report
# - The difference between the average percentage of marks the student has received since the last report and the score of the last report
# - A list of categories to suggest positive feedback in
# - A list of categories to suggest negative feedback in
# - A list of categories to suggest there was improvement in
def getStudentInfo(studentName, className, school):

    studentId = getStudentId(school, studentName)
    classId = getClassId(school, className)

    conn = connect(school)
    cursor = conn.cursor()

    cursor.execute(f"SELECT rid, date FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC")
    reports = cursor.fetchall()
    fullReports = {}
    for report in reports:
        cursor.execute(f"SELECT comment FROM reportComment WHERE rid = {report[0]}")
        comments = cursor.fetchall()
        fullReports[report[0]] = [comment[0] for comment in comments]
    cursor.execute(f"SELECT date FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC LIMIT 1")
    if cursor.fetchone() is None:
        cursor.execute(f"SELECT * FROM marks WHERE sid = {studentId} AND cid = {classId}")
        newMarks = cursor.fetchall()
        cursor.execute(f"SELECT * FROM marks WHERE cid = {classId}")
        allMarks = cursor.fetchall()
    else:
        cursor.execute(f"""SELECT * FROM marks WHERE sid = {studentId} AND cid = {classId} AND date > 
                            (SELECT date FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC LIMIT 1)""")
        newMarks = cursor.fetchall()
        cursor.execute(f"""SELECT * FROM marks WHERE cid = {classId} AND date > 
                            (SELECT date FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC LIMIT 1)""")
        allMarks = cursor.fetchall()
    cursor.execute(f"SELECT * FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC LIMIT 1")
    mostRecentReport = cursor.fetchone()
    percentages = []
    total = 0
    for mark in newMarks:
        percentages.append((mark[3] / mark[4]) * 100)
        total += (mark[3] / mark[4]) * 100
    if len(newMarks) == 0:
        average = 0
    else:
        average = int(total / len(newMarks))
    if mostRecentReport is None:
        avgDelta = 0
    else:
        avgDelta = average - mostRecentReport[5]

    if len(allMarks) == 0:
        classAvg = 0
    else:
        total = 0
        for mark in allMarks:
            total += (mark[3] / mark[4]) * 100
        classAvg = int(total / len(allMarks))

    conn.close()
    improvementOrder = []
    negativeOrder = []
    positiveOrder = []
    if avgDelta > 0:
        improvementOrder = ["performance"]
        positiveOrder = ["performance"]
    elif avgDelta <= 0:
        if average > classAvg:
            positiveOrder = ["performance"]
        else:
            negativeOrder = ["performance"]

    scores = {}
    lastImprovements = []
    for category in reportCategories:
        scores[category], li = generate_scores(category, fullReports)
        lastImprovements += li
    scores = dict(sorted(scores.items(), key=lambda item: item[1]))
    revScores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    for category in scores:
        if category not in positiveOrder:
            positiveOrder.append(category)
    for category in revScores:
        if category not in negativeOrder:
            negativeOrder.append(category)
        if category not in improvementOrder:
            improvementOrder.append(category)

    print(f"cavg: {classAvg}")

    return lastImprovements, percentages, average, avgDelta, positiveOrder, negativeOrder, improvementOrder, classAvg

# Retrieve all the students in a class
def getStudents(className, school):
    print(f"class: {className}, school: {school}")
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"SELECT cid FROM classes WHERE name = '{className}'")
    classId = cursor.fetchone()[0]
    cursor.execute(f"SELECT name FROM student JOIN classEntry ON student.sid = classEntry.sid WHERE cid = {classId}")
    students = cursor.fetchall()
    conn.close()
    return [student[0] for student in students]

# Retrieve the information from the webpage and add a new report to the database
def addReport(studentName, className, score, school, positiveComments, negativeComments, improvementComments):
    print(f"student: {studentName}, class: {className}, school: {school}, score: {score}")
    print(f"positive: {positiveComments}, negative: {negativeComments}, improvement: {improvementComments}")
    studentId = getStudentId(school, studentName)
    classId = getClassId(school, className)
    average = getStudentAverage(school, studentId, classId)
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO reports (sid, cid, date, score, average) VALUES ({studentId}, {classId}, date('now'), {score}, {average})")
    rid = cursor.lastrowid
    for comment in positiveComments:
        try:
            cursor.execute(f"INSERT INTO reportComment (rid, comment) VALUES ({rid}, '{reportCategories[comment][0]}')")
        except:
            cursor.execute(f"INSERT INTO reportComment (rid, comment) VALUES ({rid}, '{comment}')")
    for comment in negativeComments:
        try:
            cursor.execute(f"INSERT INTO reportComment (rid, comment) VALUES ({rid}, '{reportCategories[comment][1]}')")
        except:
            cursor.execute(f"INSERT INTO reportComment (rid, comment) VALUES ({rid}, '{comment}')")
    for comment in improvementComments:
        try:
            cursor.execute(f"INSERT INTO reportComment (rid, comment) VALUES ({rid}, '{reportCategories[comment][2]}')")
        except:
            cursor.execute(f"INSERT INTO reportComment (rid, comment) VALUES ({rid}, '{comment}')")
    conn.commit()
    conn.close()

    return generateNLReport(rid, school)

# Create a natural language prompt for the OpenAI API
def create_prompt(report, comments):
    prompt_start = f"""
Here is the summary of a end-of-term report for a student in a class:

Over the course of the term, the student recieved an average of {report[5]}% in the class.
"""
    for comment in comments:
        prompt_start += "\n" + comment[0]

    prompt_end = f"""

Use this summary to generate a natural language report from the perspective of the teacher addressing the student in appoximately 100 words.
Do not include any specific numbers in the report.
Begin the report with something similar to 'Over the course of the term, you have ...'"""

    return prompt_start + prompt_end

# Create a natural language report out of a report id
def generateNLReport(reportId, school):
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM reports WHERE rid = {reportId} ORDER BY date DESC LIMIT 1")
    report = cursor.fetchone()
    cursor.execute(f"SELECT comment FROM reportComment WHERE rid = {reportId}")
    comments = cursor.fetchall()
    conn.close()

    openai.api_key = api_key
    prompt = create_prompt(report, comments)
    chat_completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a model to convert a bullet-pointed end-of-term report into a natural-language one."},
            {"role": "user", "content": prompt}
        ]
    )

    return chat_completion.choices[0].message.content

# Retrieve a studentId from student name and school
def getStudentId(school, studentName):
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"SELECT sid FROM student WHERE name = '{studentName}'")
    studentId = cursor.fetchone()
    conn.close()
    return studentId[0]

# Retrieve a teacherId from teacher name and school
def getTeacherId(school, teacherName):
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"SELECT tid FROM teachers WHERE name = '{teacherName}'")
    teacherId = cursor.fetchone()
    conn.close()
    return teacherId[0]
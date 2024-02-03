import sqlite3
import openai

# Create a connection to the database
def connect(dbID):
    conn = sqlite3.connect(dbID + '.db')
    return conn


# Reetrieve user credentials from the webpage
def retrieveCredentials(request):
    username = request.form['username']
    password = request.form['password']
    return username, password

# Check if the user exists in the database
def checkUserExists(username, password, conn):
    cursor = conn.cursor()
    cursor.execute(f"SELECT school FROM teachers WHERE username = {username} AND password = {password}")
    school = cursor.fetchone()
    return school

def retrieveTeacher(request):
    username, password = retrieveCredentials(request)
    print(f"Requesting teacher: {username} with password: {password}")
    conn = connect('allTeachers')
    print(username, password)
    school = checkUserExists(username, password, conn)
    print(school)
    if school is None:
        credentialError()   # If the user does not exist, return an error to the webpage
        print("Credential error")
        conn.close()
        return
    conn.close()
    conn = connect(school)
    print("Connected to school database")
    cursor = conn.cursor()
    cursor.execute(f"SELECT tid FROM teachers WHERE username = {username}")
    tid = cursor.fetchone()
    print(f"Teacher ID: {tid}")
    cursor.execute(f"SELECT cid, name FROM classes WHERE tid = {tid}")
    results = cursor.fetchall()
    print("Classes: \n", results)
    conn.close()
    sendClasses(results)    # Send the classes to the webpage

# Retrieve the students in a class since the last report
def getStudentAverage(school, studentId, classId):
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM marks WHERE sid = {studentId} AND cid = {classId} AND date > 
                        (SELECT date FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC LIMIT 1)""")
    marks = cursor.fetchall()
    total = 0
    for mark in marks:
        total += mark[3] / mark[4]
    average = int(total / len(marks))
    conn.close()
    return average

# Retrieve information about a given student in a class. Returns:
# - A dictionary of old reports, with the key being the report ID and the value being a list of comments made in the report
# - A list of percentages of marks the student has received in the class since the last report
# - The average percentage of marks the student has received since the last report
# - The difference between the average percentage of marks the student has received since the last report and the score of the last report
def getStudentInfo(studentId, classId, school):
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"SELECT rid, date FROM reports WHERE sid = {studentId} AND cid = {classId}")
    reports = cursor.fetchall()
    fullReports = {}
    for report in reports:
        cursor.execute(f"SELECT comment FROM reportComment WHERE rid = {report[0]}")
        comments = cursor.fetchall()
        fullReports[report[0]] = comments
    cursor.execute(f"""SELECT * FROM marks WHERE sid = {studentId} AND cid = {classId} AND date > 
                        (SELECT date FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC LIMIT 1)""")
    newMarks = cursor.fetchall()
    cursor.execute(f"SELECT * FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC LIMIT 1")
    mostRecentReport = cursor.fetchone()
    percentages = []
    total = 0
    for mark in newMarks:
        percentages.append(mark[3] / mark[4])
        total += mark[3] / mark[4]
    average = int(total / len(newMarks))
    avgDelta = average - mostRecentReport[5]
    conn.close()
    return fullReports, percentages, average, avgDelta


# Retrieve the information from the webpage and add a new report to the database
def addReport(request):
    studentId = request.form['studentId']
    classId = request.form['classId']
    score = request.form['score']
    school = request.form['school']
    average = getStudentAverage(school, studentId, classId)
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO reports (sid, cid, date, score, average) VALUES ({studentId}, {classId}, date('now'), {score}, {average})")
    rid = cursor.lastrowid
    comments = request.form['comments']
    for comment in comments:
        cursor.execute(f"INSERT INTO reportComment (rid, comment) VALUES ({rid}, {comment})")
    conn.commit()
    conn.close()

# Create a natural language prompt for the OpenAI API
def create_prompt(report, comments):
    pompt_start = f"""
Here is the summary of a end-of-term report for a student in a class:

Over the course of the term, the student recieved an average of {report[5]}% in the class.
"""
    for comment in comments:
        prompt_start += "\n" + comment[0]

    prompt_end = """

Use this summary to generate a natural language report for the student of appoximately 100 words."""

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

    openai.api_key = 'some_key'
    prompt = create_prompt(report, comments)
    reponse = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )

    generated_report = response['choices'][0]['text']

    return generated_report
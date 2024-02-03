import sqlite3
import openai

api_file = open("api-key", "r")
api_key = api_file.readline()
api_key.strip()
api_file.close()

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

def generate_scores(category, reports):
    score = 0
    i = 5
    improvements = []
    for report in reports:
        for comment in reports[report]:
            if comment in reportCategories[category][0]:
                score += max(i, 0) ** 2
            elif comment in reportCategories[category][1]:
                score -= max(i, 0) ** 2
            elif comment in reportCategories[category][2]:
                if i == 5:
                    improvements.append(comment)
                score += max(i, 0) ** 1.5
    return int(score), improvements

# Retrieve information about a given student in a class. Returns:
# - A list of what the student was told to improve on in the last report
# - A list of percentages of marks the student has received in the class since the last report
# - The average percentage of marks the student has received since the last report
# - The difference between the average percentage of marks the student has received since the last report and the score of the last report
# - A list of categories to suggest positive feedback in
# - A list of categories to suggest negative feedback in
# - A list of categories to suggest there was improvement in
def getStudentInfo(studentId, classId, school):
    conn = connect(school)
    cursor = conn.cursor()
    cursor.execute(f"SELECT rid, date FROM reports WHERE sid = {studentId} AND cid = {classId} ORDER BY date DESC")
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
    improvementOrder = []
    negativeOrder = []
    positiveOrder = []
    if avgDelta > 0:
        improvementOrder = ["performance"]
        positiveOrder = ["performance"]
    elif avgDelta < 0:
        negativeOrder = ["performance"]
    else:
        positiveOrder = ["performance"]
    scores = {}
    for category in reportCategories:
        scores[category], lastImprovements = generate_scores(category, fullReports)
    scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    revScores = dict(sorted(scores.items(), key=lambda item: item[1]))
    for category in scores:
        if scores[category] not in positiveOrder:
            improvementOrder.append(category)
    for category in revScores:
        if scores[category] not in negativeOrder:
            improvementOrder.append(category)
        if scores[category] not in improvementOrder:
            improvementOrder.append(category)
    return lastImprovements, percentages, average, avgDelta, positiveOrder, negativeOrder, improvementOrder


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
    positiveComments = request.form['pComments']
    negativeComments = request.form['nComments']
    improvementComments = request.form['iComments']
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

# Create a natural language prompt for the OpenAI API
def create_prompt(report, comments):
    prompt_start = f"""
Here is the summary of a end-of-term report for a student in a class:

Over the course of the term, the student recieved an average of {report[5]}% in the class.
"""
    for comment in comments:
        prompt_start += "\n" + comment[0]

    prompt_end = """

Overall, the teacher feels that the student peformed {report[4]} out of 5 in the class.
Use this summary to generate a natural language report for the student from the perspective of the teacher in appoximately 100 words.
Do not include any specific numbers in the report."""

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
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )

    generated_report = response['choices'][0]['text']

    return generated_report
import sqlite3
import os
from datetime import datetime

# Create a school
def createSchool(school):
    conn = sqlite3.connect('allTeachers.db')
    cursor = conn.cursor()
    exists = cursor.execute(f"SELECT * FROM schools WHERE school = '{school}'")
    if exists.fetchone() is not None:
        print("School already exists")
        conn.close()
        return
    cursor.execute(f"INSERT INTO schools (school) VALUES ('{school}')")
    conn.commit()
    conn.close()

    print("School added to allTeachers.db. Creating tables...")

    # Create a database for the school
    conn = sqlite3.connect(school + '.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE student (sid INTEGER PRIMARY KEY, name TEXT NOT NULL)')
    cursor.execute('CREATE TABLE teachers (tid INTEGER PRIMARY KEY, name TEXT NOT NULL)')
    cursor.execute('CREATE TABLE tasks (taskid INTEGER PRIMARY KEY, name TEXT NOT NULL)')
    cursor.execute('CREATE TABLE classes (cid INTEGER PRIMARY KEY, name TEXT NOT NULL, tid INTEGER NOT NULL, FOREIGN KEY (tid) REFERENCES teachers(tid))')
    cursor.execute('CREATE TABLE classEntry (sid INTEGER NOT NULL, cid INTEGER NOT NULL,  PRIMARY KEY(sid, cid), FOREIGN KEY (sid) REFERENCES student(sid), FOREIGN KEY (cid) REFERENCES classes(cid))')
    cursor.execute('CREATE TABLE marks (sid INTEGER NOT NULL, cid INTEGER NOT NULL, taskid INTEGER NOT NULL, mark INTEGER NOT NULL, maxMark INTEGER NOT NULL, date DATE NOT NULL, comments TEXT,  PRIMARY KEY(sid, taskid), FOREIGN KEY (sid) REFERENCES student(sid), FOREIGN KEY (cid) REFERENCES classes(cid), FOREIGN KEY (taskid) REFERENCES tasks(taskid))')
    cursor.execute('CREATE TABLE reports (rid INTEGER PRIMARY KEY, sid INTEGER NOT NULL, cid INTEGER NOT NULL, date DATE NOT NULL, score INTEGER NOT NULL, average INTEGER NOT NULL, FOREIGN KEY (sid) REFERENCES student(sid), FOREIGN KEY (cid) REFERENCES classes(cid))')
    cursor.execute('CREATE TABLE reportComment (rid INTEGER NOT NULL, comment TEXT NOT NULL, PRIMARY KEY (rid, comment), FOREIGN KEY (rid) REFERENCES reports(rid))')
    conn.commit()
    conn.close()
    print(f"{school} Setup Complete")

# Add a teacher to a school
def addTeacher(school, username, password):
    conn = sqlite3.connect('allTeachers.db')
    cursor = conn.cursor()
    exists = cursor.execute(f"SELECT * FROM teachers WHERE username = '{username}'")
    if exists.fetchone() is not None:
        print("Teacher already exists")
        conn.close()
        return
    cursor.execute(f"INSERT INTO teachers (school, username, password) VALUES ('{school}', '{username}', '{password}')")
    conn.commit()
    conn.close()

    # Add the teacher to the school database
    conn = sqlite3.connect(school + '.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO teachers (name) VALUES ('{username}')")
    conn.commit()
    conn.close()
    print(f"{username} added to {school} with password {password}")

def removeSchool(school):
    if os.path.exists(f'{school}.db'):
        os.remove(f'{school}.db')
        print(f"{school}.db removed")
    conn = sqlite3.connect('allTeachers.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM schools WHERE school = '{school}'")
    conn.commit()
    conn.close()
    print(f"{school} removed from allTeachers.db")
def addStudent(school, name):
    conn = sqlite3.connect(f'{school}.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO student (name) VALUES ('{name}')")
    conn.commit()
    conn.close()
    print(f"{name} added to {school}")
def addClass(school, name, teacher):
    conn = sqlite3.connect(f'{school}.db')
    cursor = conn.cursor()

    # Get the teacher id
    cursor.execute(f"SELECT tid FROM teachers WHERE name = '{teacher}'")
    tid = cursor.fetchone()
    if tid is None:
        print(f"Teacher {teacher} does not exist")
        conn.close()
        return
    cursor.execute(f"INSERT INTO classes (name, tid) VALUES ('{name}', {tid[0]})")
    conn.commit()
    conn.close()
    print(f"{name} added to {school}")
def addEntry(school, classname, student):
    conn = sqlite3.connect(f'{school}.db')
    cursor = conn.cursor()

    # Get the student id
    cursor.execute(f"SELECT sid FROM student WHERE name = '{student}'")
    sid = cursor.fetchone()
    if sid is None:
        print(f"Student {student} does not exist")
        conn.close()
        return

    # Get the class id
    cursor.execute(f"SELECT cid FROM classes WHERE name = '{classname}'")
    cid = cursor.fetchone()
    if cid is None:
        print(f"Class {classname} does not exist")
        conn.close()
        return
    cursor.execute(f"INSERT INTO classEntry (sid, cid) VALUES ({sid[0]}, {cid[0]})")
    conn.commit()
    conn.close()
    print(f"{student} added to {classname}")
def addTask(school, name):
    conn = sqlite3.connect(f'{school}.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO tasks (name) VALUES ('{name}')")
    conn.commit()
    conn.close()
    print(f"{name} added to {school}")
def addMark(school, classname, student, task, mark, maxMark, date, comments):
    conn = sqlite3.connect(f'{school}.db')
    cursor = conn.cursor()

    # Get the student id
    cursor.execute(f"SELECT sid FROM student WHERE name = '{student}'")
    sid = cursor.fetchone()
    if sid is None:
        print(f"Student {student} does not exist")
        conn.close()
        return

    # Get the class id
    cursor.execute(f"SELECT cid FROM classes WHERE name = '{classname}'")
    cid = cursor.fetchone()
    if cid is None:
        print(f"Class {classname} does not exist")
        conn.close()
        return

    # Get the task id
    cursor.execute(f"SELECT taskid FROM tasks WHERE name = '{task}'")
    taskid = cursor.fetchone()
    if taskid is None:
        print(f"Task {task} does not exist")
        conn.close()
        return
    cursor.execute(f"INSERT INTO marks (sid, cid, taskid, mark, maxMark, date, comments) VALUES ({sid[0]}, {cid[0]}, {taskid[0]}, {mark}, {maxMark}, '{datetime.strptime(date, '%d/%m/%Y')}', '{comments}')")
    conn.commit()
    conn.close()
    print(f"{student} marked in {classname}")
def list(school, table):
    conn = sqlite3.connect(f'{school}.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    print(cursor.fetchall())
    conn.close()
def sqls(database, command):
    conn = sqlite3.connect(f'{database}.db')
    cursor = conn.cursor()
    commandBuilt = ""
    for i in range(2, len(command)):
        commandBuilt += command[i] + " "
    try:
        cursor.execute(commandBuilt)
        conn.commit()
    except:
        print(f"Invalid SQL {commandBuilt}")
    conn.close()
def sqlg(database, command):
    conn = sqlite3.connect(f'{database}.db')
    cursor = conn.cursor()
    commandBuilt = ""
    for i in range(2, len(command)):
        commandBuilt += command[i] + " "
    try:
        cursor.execute(commandBuilt)
        print(cursor.fetchall())
    except:
        print(f"Invalid SQL {commandBuilt}")
    conn.close()
def addReport(school, student, classname, date, score, average, comments):
    conn = sqlite3.connect(f'{school}.db')
    cursor = conn.cursor()

    # Get the student id
    cursor.execute(f"SELECT sid FROM student WHERE name = '{student}'")
    sid = cursor.fetchone()
    if sid is None:
        print(f"Student {student} does not exist")
        conn.close()
        return

    # Get the class id
    cursor.execute(f"SELECT cid FROM classes WHERE name = '{classname}'")
    cid = cursor.fetchone()
    if cid is None:
        print(f"Class {classname} does not exist")
        conn.close()
        return
    cursor.execute(f"INSERT INTO reports (sid, cid, date, score, average) VALUES ({sid[0]}, {cid[0]}, '{datetime.strptime(date, '%d/%m/%Y')}', {score}, {average})")
    
    # Get the report id
    cursor.execute(f"SELECT rid FROM reports WHERE sid = {sid[0]} AND cid = {cid[0]} AND date = '{datetime.strptime(date, '%d/%m/%Y')}'")
    rid = cursor.fetchone()[0]
    
    for comment in comments:
        cursor.execute(f"INSERT INTO reportComment (rid, comment) VALUES ({rid}, '{comment}')")
    conn.commit()
    conn.close()
    print(f"{student} reported in {classname}")

def makeExample():
    rcs = {
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

    removeSchool("example")
    createSchool("example")
    addTeacher("example", "teacher1", "password")
    addStudent("example", "student1")
    addStudent("example", "student2")
    addStudent("example", "student3")
    addClass("example", "maths", "teacher1")
    addClass("example", "english", "teacher1")
    addEntry("example", "maths", "student1")
    addEntry("example", "maths", "student2")
    addEntry("example", "maths", "student3")
    addTask("example", "maths_hw1")
    addTask("example", "maths_hw2")
    addTask("example", "maths_hw3")
    addTask("example", "maths_hw4")
    addMark("example", "maths", "student1", "maths_hw1", 10, 10, "01/01/2020", "Good")
    addMark("example", "maths", "student2", "maths_hw1", 5, 10, "01/01/2020", "Bad")
    addMark("example", "maths", "student3", "maths_hw1", 5, 10, "01/01/2020", "Bad")
    addMark("example", "maths", "student1", "maths_hw2", 9, 10, "01/02/2020", "Good")
    addMark("example", "maths", "student2", "maths_hw2", 3, 10, "01/02/2020", "Bad")
    addMark("example", "maths", "student3", "maths_hw2", 4, 10, "01/02/2020", "Bad")
    addMark("example", "maths", "student1", "maths_hw3", 10, 10, "01/01/2021", "Good")
    addMark("example", "maths", "student2", "maths_hw3", 3, 10, "01/01/2021", "Bad")
    addMark("example", "maths", "student3", "maths_hw3", 8, 10, "01/01/2021", "Good")
    addMark("example", "maths", "student1", "maths_hw4", 8, 10, "01/01/2021", "Good")
    addMark("example", "maths", "student2", "maths_hw4", 1, 10, "01/01/2021", "Bad")
    addMark("example", "maths", "student3", "maths_hw4", 9, 10, "01/01/2021", "Good")
    addReport("example", "student1", "maths", "01/12/2020", 5, 90, [rcs["performance"][0], rcs["attendance"][1], rcs["organisation"][2], rcs["respect"][2]])
    addReport("example", "student2", "maths", "01/12/2020", 2, 40, [rcs["performance"][1], rcs["attendance"][1], rcs["homework"][1], rcs["punctuality"][2]])
    addReport("example", "student3", "maths", "01/12/2020", 1, 40, [rcs["performance"][1], rcs["attendance"][2], rcs["homework"][1], rcs["punctuality"][0]])
    print("Example school created")



while True:
    command = input(">: ")
    if command.lower() == "q":
        break
    command = command.split()
    if (len(command) < 1):
        print("Invalid command. Try again or type 'q' to quit. Type 'help' for help.")
        continue
    elif command[0].lower() == "help":
        print("school <school>: create a school")
        print("teacher <school> <username> <password>: add a teacher to a school")
        print("remove <school>: remove a school and its database")
        print("student <school> <name>: add a student to a school")
        print("class <school> <name> <teacher username>: add a class to a school")
        print("entry <school> <class> <student>: add a student to a class")
        print("task <school> <name>: add a task to a school")
        print("mark <school> <class> <student> <task> <mark> <maxMark> <date> <comments>: add a mark to a student")
        print("list <school> <table>: list all the entries in a table")
        print("sqls <database> <sql>: execute sql on any database")
        print("sqlg <database> <sql>: execute sql on any database and print the result")
        print("example: create an example school")
        print("q: quit")
    elif command[0].lower() == "school":
        createSchool(command[1])
    elif command[0].lower() == "teacher":
        if (len(command) < 4):
            print("Invalid command. Try again or type 'q' to quit. Type 'help' for help.")
            continue
        else:
            addTeacher(command[1], command[2], command[3])
    elif command[0].lower() == "student":
        addStudent(command[1], command[2])
    elif command[0].lower() == "class":
        addClass(command[1], command[2], command[3])
    elif command[0].lower() == "entry":
        addEntry(command[1], command[2], command[3])
    elif command[0].lower() == "task":
        addTask(command[1], command[2])
    elif command[0].lower() == "mark":
        addMark(command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8])
    elif command[0].lower() == "list":
        list(command[1], command[2])
    elif command[0].lower() == "sqls":
        sqls(command[1], command)
    elif command[0].lower() == "sqlg":
        sqlg(command[1], command)
    elif command[0].lower() == "remove":
        removeSchool(command[1])
    elif command[0].lower() == "example":
        makeExample()
    else:
        print("Invalid command. Try again or type 'q' to quit.")
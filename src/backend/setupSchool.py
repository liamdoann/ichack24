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
        conn = sqlite3.connect(f'{command[1]}.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO student (name) VALUES ('{command[2]}')")
        conn.commit()
        conn.close()
        print(f"{command[2]} added to {command[1]}")
    elif command[0].lower() == "class":
        conn = sqlite3.connect(f'{command[1]}.db')
        cursor = conn.cursor()

        # Get the teacher id
        cursor.execute(f"SELECT tid FROM teachers WHERE name = '{command[3]}'")
        tid = cursor.fetchone()
        if tid is None:
            print(f"Teacher {command[3]} does not exist")
            conn.close()
            continue
        cursor.execute(f"INSERT INTO classes (name, tid) VALUES ('{command[2]}', {tid[0]})")
        conn.commit()
        conn.close()
        print(f"{command[2]} added to {command[1]}")
    elif command[0].lower() == "entry":
        conn = sqlite3.connect(f'{command[1]}.db')
        cursor = conn.cursor()

        # Get the student id
        cursor.execute(f"SELECT sid FROM student WHERE name = '{command[3]}'")
        sid = cursor.fetchone()
        if sid is None:
            print(f"Student {command[3]} does not exist")
            conn.close()
            continue

        # Get the class id
        cursor.execute(f"SELECT cid FROM classes WHERE name = '{command[2]}'")
        cid = cursor.fetchone()
        if cid is None:
            print(f"Class {command[2]} does not exist")
            conn.close()
            continue
        cursor.execute(f"INSERT INTO classEntry (sid, cid) VALUES ({sid[0]}, {cid[0]})")
        conn.commit()
        conn.close()
        print(f"{command[3]} added to {command[2]}")
    elif command[0].lower() == "task":
        conn = sqlite3.connect(f'{command[1]}.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO tasks (name) VALUES ('{command[2]}')")
        conn.commit()
        conn.close()
        print(f"{command[2]} added to {command[1]}")
    elif command[0].lower() == "mark":
        conn = sqlite3.connect(f'{command[1]}.db')
        cursor = conn.cursor()

        # Get the student id
        cursor.execute(f"SELECT sid FROM student WHERE name = '{command[3]}'")
        sid = cursor.fetchone()
        if sid is None:
            print(f"Student {command[3]} does not exist")
            conn.close()
            continue

        # Get the class id
        cursor.execute(f"SELECT cid FROM classes WHERE name = '{command[2]}'")
        cid = cursor.fetchone()
        if cid is None:
            print(f"Class {command[2]} does not exist")
            conn.close()
            continue

        # Get the task id
        cursor.execute(f"SELECT taskid FROM tasks WHERE name = '{command[4]}'")
        taskid = cursor.fetchone()
        if taskid is None:
            print(f"Task {command[4]} does not exist")
            conn.close()
            continue
        cursor.execute(f"INSERT INTO marks (sid, cid, taskid, mark, maxMark, date, comments) VALUES ({sid[0]}, {cid[0]}, {taskid[0]}, {command[5]}, {command[6]}, '{datetime.strptime(command[7], '%d/%m/%Y')}', '{command[8]}')")
        conn.commit()
        conn.close()
        print(f"{command[3]} marked in {command[2]}")
    elif command[0].lower() == "list":
        conn = sqlite3.connect(f'{command[1]}.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {command[2]}")
        print(cursor.fetchall())
        conn.close()
    elif command[0].lower() == "sqls":
        conn = sqlite3.connect(f'{command[1]}.db')
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
    elif command[0].lower() == "sqlg":
        conn = sqlite3.connect(f'{command[1]}.db')
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
    elif command[0].lower() == "remove":
        if os.path.exists(f'{command[1]}.db'):
            os.remove(f'{command[1]}.db')
            print(f"{command[1]}.db")
        conn = sqlite3.connect('allTeachers.db')
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM schools WHERE school = '{command[1]}'")
        conn.commit()
        conn.close()
        print(f"{command[1]} removed from allTeachers.db")
    else:
        print("Invalid command. Try again or type 'q' to quit.")
import sqlite3

# Create a school
def createSchool(school):
    conn = sqlite3.connect('allTeachers.db')
    cursor = conn.cursor()
    exists = cursor.execute(f"SELECT * FROM schools WHERE school = '{school}'")
    if exists.fetchone() is not None:
        print("School already exists")
        conn.close()
        return
    cursor.execute(f'INSERT INTO schools VALUES ({school})')
    conn.commit()
    conn.close()

    # Create a database for the school
    conn = sqlite3.connect(school + '.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE student (sid INTEGER PRIMARY KEY, name TEXT NOT NULL)')
    cursor.execute('CREATE TABLE teachers (tid INTEGER PRIMARY KEY, name TEXT NOT NULL)')
    cursor.execute('CREATE TABLE tasks (taskid INTEGER PRIMARY KEY, name TEXT NOT NULL)')
    cursor.execute('CREATE TABLE classes (cid INTEGER PRIMARY KEY, name TEXT NOT NULL, tid INTEGER NOT NULL, FOREIGN KEY (teacher) REFERENCES teachers(tid))')
    cursor.execute('CREATE TABLE classEntry (sid INTEGER NOT NULL, cid INTEGER NOT NULL, FOREIGN KEY (sid) REFERENCES student(sid), FOREIGN KEY (cid) REFERENCES classes(cid))')
    cursor.execute('CREATE TABLE marks (sid INTEGER NOT NULL, cid INTEGER NOT NULL, taskid INTEGER NOT NULL, mark INTEGER NOT NULL, maxMark INTEGER NOT NULL, date DATE NOT NULL, comments TEXT, FOREIGN KEY (sid) REFERENCES student(sid), FOREIGN KEY (cid) REFERENCES classes(cid), FOREIGN KEY (taskid) REFERENCES tasks(taskid))')
    cursor.execute('CREATE TABLE reports (rid INTEGER PRIMARY KEY, sid INTEGER NOT NULL, cid INTEGER NOT NULL, date DATE NOT NULL, score INTEGER NOT NULL, average INTEGER NOT NULL, FOREIGN KEY (sid) REFERENCES student(sid), FOREIGN KEY (cid) REFERENCES classes(cid))')
    cursor.execute('CREATE TABLE reportComment (rid INTEGER NOT NULL, comment TEXT NOT NULL, FOREIGN KEY (rid) REFERENCES reports(rid)')
    conn.commit()
    conn.close()
    print("Setup Complete")

# Add a teacher to a school
def addTeacher(school, username, password):
    conn = sqlite3.connect('allTeachers.db')
    cursor = conn.cursor()
    exists = cursor.execute(f"SELECT * FROM teachers WHERE username = '{username}'")
    if exists.fetchone() is not None:
        print("Teacher already exists")
        conn.close()
        return
    cursor.execute(f'INSERT INTO teachers VALUES ({school}, {username}, {password})')
    conn.commit()
    conn.close()

    # Add the teacher to the school database
    conn = sqlite3.connect(school + '.db')
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO teachers (name) VALUES ({username})')
    conn.commit()
    conn.close()
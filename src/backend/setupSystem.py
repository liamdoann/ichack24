import sqlite3

# Setup the system
def setup():
    # Create a database for all the teachers
    conn = sqlite3.connect('allTeachers.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE schools (school TEXT PRIMARY KEY)')
    cursor.execute('CREATE TABLE teachers (school TEXT PRIMARY KEY, username TEXT PRIMARY KEY, password TEXT NOT NULL, FOREIGN KEY (school) REFERENCES schools(school))')
    conn.commit()
    conn.close()

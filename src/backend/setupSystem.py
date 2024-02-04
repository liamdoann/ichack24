import sqlite3
import os

# Setup the system
def setup():
    # Create a database for all the teachers
    if os.path.exists('allTeachers.db'):
        os.remove('allTeachers.db')

    conn = sqlite3.connect('allTeachers.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE schools (school TEXT PRIMARY KEY)')
    cursor.execute('CREATE TABLE teachers (school TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL,  PRIMARY KEY(school, username), FOREIGN KEY (school) REFERENCES schools(school))')
    conn.commit()
    conn.close()

setup()
print("setup")
import sqlite3

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

def main(request):
    username, password = retrieveCredentials(request)
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

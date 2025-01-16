#!/usr/bin/env python3
import cgi
import cgitb
import mysql.connector
import bcrypt
import re
from getpass import getpass

# Enable CGI error handling
cgitb.enable()

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="priya",  # Make sure to use your actual database credentials
    database="usersdb"
)
cursor = conn.cursor()

# Function to register a new user
def register_user():
    form = cgi.FieldStorage()
    username = form.getvalue("username")
    email = form.getvalue("email")
    password = form.getvalue("password")
    confirm_password = form.getvalue("confirm_password")

    if password != confirm_password:
        return "Passwords do not match!"

    # Password validation: 8 characters, 1 special char, 1 uppercase
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[@#$%^&+=]', password):
        return "Password must be at least 8 characters long, contain 1 uppercase letter and 1 special character."

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Set role_id to 3 (User) by default
    cursor.execute("SELECT id FROM roles WHERE name = 'User'")
    role_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO users (username, email, password, role_id) VALUES (%s, %s, %s, %s)",
                   (username, email, hashed_password, role_id))
    conn.commit()

    return f"User {username} registered successfully."

# Function to log in a user
def login_user():
    form = cgi.FieldStorage()
    username = form.getvalue("username")
    password = form.getvalue("password")

    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user is None:
        return "User not found!"

    stored_password = user[0]
    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        return f"Login successful! Welcome {username}"
    else:
        return "Incorrect password!"

# Function to render HTML files
def render_html(page_name, content=""):
    with open(f'templates/{page_name}', 'r') as file:
        html = file.read()
    return html.replace("{{content}}", content)

# Admin Dashboard
def admin_dashboard():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    user_table = "<table><tr><th>Username</th><th>Email</th><th>Role</th><th>Action</th></tr>"
    for user in users:
        user_table += f"<tr><td>{user[1]}</td><td>{user[2]}</td><td>{user[4]}</td><td><form action='assign_role.py' method='POST'><select name='role'><option value='2'>Manager</option><option value='3'>User</option></select><input type='hidden' name='username' value='{user[1]}'><input type='submit' value='Assign Role'></form></td></tr>"
    user_table += "</table>"

    return render_html('admin_dashboard.html', user_table)

# Main CGI logic
def main():
    print("Content-Type: text/html\n")  # CGI header for HTML

    form = cgi.FieldStorage()
    action = form.getvalue("action")

    if action == "register":
        content = register_user()
        print(render_html("register.html", content))
    elif action == "login":
        content = login_user()
        print(render_html("login.html", content))
    elif action == "admin_dashboard":
        content = admin_dashboard()
        print(content)
    else:
        print(render_html("index.html"))

if __name__ == "__main__":
    main()

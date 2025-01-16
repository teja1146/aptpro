import mysql.connector
import cgi

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="priya",
    database="usersdb"
)
cursor = conn.cursor()

# Retrieve form data
form = cgi.FieldStorage()
username = form.getvalue("username")
role_id = form.getvalue("role")

# Update the user's role in the database
cursor.execute("""
    UPDATE users
    SET role_id = %s
    WHERE username = %s
""", (role_id, username))

conn.commit()

# Provide a confirmation or redirection (optional)
print("Content-Type: text/html")
print()  # Required for CGI response
print("<html><body>")
print("<h3>Role updated successfully!</h3>")
print("<a href='admin_dashboard.html'>Back to Dashboard</a>")
print("</body></html>")

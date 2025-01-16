import mysql.connector
from mysql.connector import Error

# Database connection function
def get_db_connection():
    try:
        # Change these details to match your actual database configuration
        conn = mysql.connector.connect(
            host="localhost",
            user="root",             # Your database username
            password="priya",     # Your database password
            database="usersdb"  # Your database name
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Example function to fetch users (or any other query)
def fetch_users():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")  # Your query to fetch users
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    return []

# Example function to update the user role
def update_user_role(username, role_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET role_id = %s
            WHERE username = %s
        """, (role_id, username))
        conn.commit()
        cursor.close()
        conn.close()


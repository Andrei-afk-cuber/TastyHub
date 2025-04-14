import sqlite3

# Function for check password
def toggle_password(p_block, show_password_var):
    if show_password_var.get():
        p_block.configure(show="")
    else:
        p_block.configure(show="*")

def get_database_connection():
    # Open a database connection
    db = sqlite3.connect('users_database.db')
    cursor = db.cursor()
    return db, cursor

def close_database_connection(db):
    # Close the database connection
    if db:
        db.close()

# Function for check username and password
def check_login(username, password):
    db, cursor = get_database_connection()
    try:

        # Check if the provided username and password match a record in the users table
        cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()

        # If a matching record is found, return True for a successful login
        if result:
            return True

    except sqlite3.Error as e:
        # Handle any potential database errors here
        print("SQLite error:", e)

    finally:
        # Close the database connection
        close_database_connection(db)

    # Return False for unsuccessful login
    return False

def register_user(username, password):
    db, cursor = get_database_connection()
    try:
        # Create a Users table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
        """)

        # Insert user data into the Users table
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        # Commit the changes and close the database connection
        db.commit()

        return True # Registration successful

    except sqlite3.IntegrityError:
        return False # Username or email is already in use

    finally:
        close_database_connection(db)
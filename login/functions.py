import sqlite3

# Функция для показа/скрытия пароля при нажатии check_box
def toggle_password(p_block, show_password_var):
    if show_password_var.get():
        p_block.configure(show="")
    else:
        p_block.configure(show="*")

# Функция создания соединения с БД
def get_database_connection():
    # Открываем соединение с БД
    db = sqlite3.connect('users_database.db')
    cursor = db.cursor()
    return db, cursor

def close_database_connection(db):
    # Закрываем соединение с БД
    if db:
        db.close()

# Функция для проверки наличия пароля и логина в БД
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

# Функция регистрации пользователя
def register_user(username, password):
    db, cursor = get_database_connection()
    try:
        # Создание таблицы users если она не найдена
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
        """)

        # Вставляем данные пользователя в БД
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        # Сохраняем изменения и делаем их коммит
        db.commit()

        return True # Регистрация прошла успешно

    except sqlite3.IntegrityError:
        return False # В случае, если данные уже существуют в БД

    finally:
        close_database_connection(db)
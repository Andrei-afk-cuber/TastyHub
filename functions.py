import sqlite3

# Функция создания соединения с БД
def get_database_connection():
    # Открываем соединение с БД
    db = sqlite3.connect("recipes_database.db")
    cursor = db.cursor()
    return db, cursor

def close_database_connection(db):
    # Закрываем соединение с БД
    if db:
        db.close()

# Функция загрузки рецептов
def load_recipes():
    db, cursor = get_database_connection()

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_name TEXT NOT NULL,
        cook_time INTEGER NOT NULL,
        description TEXT NOT NULL,
        )
        """)
    except:
        pass
    finally:
        close_database_connection(db)

# Функция сохранения рецептов
def save_recipe():
    db, cursor = get_database_connection()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_name TEXT NOT NULL,
            cook_time INTEGER NOT NULL,
            description TEXT NOT NULL,
            )
            """)
    except:
        pass
    finally:
        close_database_connection(db)
import sqlite3
import os
import shutil
from classes import Recipe, User

# Функция создания соединения с БД
def get_database_connection():
    # Открываем соединение с БД
    db = sqlite3.connect("database.db")
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
            author_name TEXT NOT NULL,
            recipe_name TEXT NOT NULL,
            cook_time INTEGER NOT NULL,
            description TEXT NOT NULL,
            picture_path TEXT NOT NULL,
        )
        """)
    except:
        pass
    finally:
        close_database_connection(db)

# Функция сохранения рецептов
def save_recipe(recipe):

    # Преобразуем необходимые элементы для размещения в БД
    products = ', '.join(recipe.getProductList())
    image_filename = os.path.basename(recipe.getPicturePath())

    # Сохраняем картинку блюда в папке с проектом
    copy_image(recipe.getPicturePath())

    db, cursor = get_database_connection()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_name TEXT NOT NULL,
            recipe_name TEXT NOT NULL,
            description TEXT NOT NULL,
            cooking_time INTEGER NOT NULL,
            products TEXT NOT NULL,
            picture_path TEXT NOT NULL,
            confirmed INTEGER NOT NULL DEFAULT 0
            )
            """)

        # Вставляем данные в БД
        cursor.execute("INSERT INTO recipes (author_name, recipe_name, description, cooking_time, products, picture_path, confirmed) VALUES (?, ?, ? , ?, ?, ?, ?)",
                       (recipe.getAuthor(), recipe.getName(), recipe.getDescription(), recipe.getCookingTime(), products, image_filename, int(recipe.getConfirmed())))
        db.commit()

    except sqlite3.Error as e:
        print(f"Ошибка при сохранении рецепта: {e}")
    finally:
        close_database_connection(db)

# Функция копирования изображений из одной папки в другую
def copy_image(source_path, destination_folder="recipe_images"):
    try:
        # Проверяем существование исходного файла
        if not os.path.exists(source_path):
            print(f"Ошибка: фйла {source_path} не существует")
            return None

        # Проверяем что это файл (а не папка)
        if not os.path.isfile(source_path):
            print(f"Ошибка: {source_path} не является файлом")
            return None

        # Создаем целевую папку, если её нет
        os.makedirs(destination_folder, exist_ok=True)

        # Получаем имя файла из исходного пути
        file_name = os.path.basename(source_path)

        # Формируем полный путь назначения
        destination_path = os.path.join(destination_folder, file_name)

        # Копируем файл
        shutil.copy2(source_path, destination_path)
        print(f"Изображение скопировано в {destination_path}")
        return destination_path

    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        return None
import sqlite3
import os
import shutil

from customtkinter import CTkLabel

from classes import Recipe, User
from tkinter import messagebox
from PIL import ImageTk, Image
import customtkinter as ctk
from login.config import theme

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
def load_recipes(only_confirmed=True, limit=None, by_author=None, by_name=None):
    db, cursor = get_database_connection()
    recipes = []

    try:
        # Создаем таблицу, если не существует
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

        query = "SELECT * FROM recipes"
        params = []
        conditions = []

        if only_confirmed:
            conditions.append("confirmed = 1")

        if by_author:
            conditions.append("author_name = ?")
            params.append(by_author)

        if by_name:
            conditions.append("recipe_name LIKE ?")
            params.append(f"%{by_name}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)

        # Выполняем запрос
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]

        # Создаем объекты Recipe
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            try:
                recipes.append(Recipe(
                    id=row_dict["id"],
                    author=row_dict['author_name'],
                    name=row_dict['recipe_name'],
                    description=row_dict['description'],
                    picture_path=row_dict['picture_path'],
                    cooking_time=row_dict['cooking_time'],
                    product_list=[p.strip() for p in row_dict['products'].split(',')],
                    confirmed=bool(row_dict['confirmed'])
                ))
            except Exception as e:
                print(f"Ошибка создания объекта Recipe: {e}")
                continue

        return recipes

    except sqlite3.Error as e:
        print(f"Ошибка: ", e)
        return None

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

def update_recipe_by_id(old_recipe, new_recipe):
    db, cursor = get_database_connection()
    try:
        # Получаем соединение с БД
        db, cursor = get_database_connection()

        # Получаем ID рецепта
        recipe_id = old_recipe.getId()
        if not recipe_id:
            raise ValueError("Рецепт не содержит ID")

        # Устанавливаем значение confirmed в False
        new_recipe.setConfirmed(False)

        # Преобразуем необходимые элементы для размещения в БД
        products = ', '.join(new_recipe.getProductList())
        image_filename = os.path.basename(new_recipe.getPicturePath())

        # 1. Удаляем старую версию рецепта
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))

        # 2. Вставляем новую версию с тем же ID
        cursor.execute("""
                    INSERT INTO recipes (
                        id, 
                        author_name, 
                        recipe_name, 
                        description, 
                        cooking_time, 
                        products, 
                        picture_path, 
                        confirmed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
            recipe_id,
            new_recipe.getAuthor(),
            new_recipe.getName(),
            new_recipe.getDescription(),
            new_recipe.getCookingTime(),
            products,
            image_filename,
            int(new_recipe.getConfirmed())
        ))

        db.commit()
        return True
    except sqlite3.Error as e:
        print(f"Ошибка обновления рецепта: {e}")
        if db:
            db.rollback()
        return False
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        if db:
            db.rollback()
        return False
    finally:
        if db:
            close_database_connection(db)

# Класс карточки рецепта, с возможностью редактирования
class EditableRecipeCard(ctk.CTkFrame):
    def __init__(self, master, recipe, main_program):
        super().__init__(
            master,
            fg_color=theme['recipe_card_fg_color'],
            corner_radius=10,
            border_width=1,
            border_color="#e0e0e0",
            width=220,
            height=320
        )
        self.main_program = main_program
        self.recipe = recipe
        self.ctk_image = None  # Для хранения CTkImage

        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)

        # Заголовок (название рецепта)
        self.name_label = ctk.CTkLabel(
            master=self,
            text=recipe.getName(),
            font=("Aria", 14, "bold"),
            wraplength=180,
            text_color=theme['text_color'],
            height=40
        )
        self.name_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="n")

        # Метка "не подтвержден" для рецепта
        if not recipe.getConfirmed():
            self.name_label.configure(text_color="red")

        # Изображение (используем CTkLabel + CTkImage)
        self.image_label = ctk.CTkLabel(
            self,
            text="",
            width=180,
            height=120,
            fg_color="transparent",
            corner_radius=8
        )
        self.image_label.grid(row=1, column=0, padx=10, pady=5)

        # Краткое описание
        short_desc = (recipe.getDescription()[:100] + "...") if len(
            recipe.getDescription()) > 100 else recipe.getDescription()
        self.desc_label = ctk.CTkLabel(
            self,
            text=short_desc,
            font=("Arial", 11),
            wraplength=180,
            justify="left",
            height=60
        )
        self.desc_label.grid(row=2, column=0, padx=10, pady=5)

        # Контейнер для кнопок
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=3, column=0, pady=(5, 10))

        # Кнопка "Удалить"
        self.delete_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Удалить",
            width=100,
            height=30,
            fg_color="#ff4d4d",
            hover_color="#ff1a1a",
            text_color="white",
            command=self.confirm_delete
        )
        self.delete_btn.pack(side="left", padx=5)

        # Кнопка "Редактировать"
        self.edit_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Редактировать",
            width=100,
            height=30,
            fg_color=theme['fg_color'],
            hover_color=theme['hover_color'],
            command=lambda: self.main_program.open_edit_recipe_frame(recipe)
        )
        self.edit_btn.pack(side="left", padx=5)

        self.load_recipe_image()

    def load_recipe_image(self):
        try:
            image_path = os.path.join("recipe_images", self.recipe.getPicturePath())

            if os.path.exists(image_path):
                # Создаем CTkImage
                self.ctk_image = ctk.CTkImage(
                    light_image=Image.open(image_path),
                    dark_image=Image.open(image_path),
                    size=(180, 120)  # Размеры можно настроить
                )

                # Устанавливаем изображение
                self.image_label.configure(
                    image=self.ctk_image,
                    text=""
                )
            else:
                self.image_label.configure(
                    text="Изображение не найдено",
                    font=('Century Gothic', 12),
                    text_color="gray"
                )
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.image_label.configure(
                text="Ошибка загрузки",
                font=('Century Gothic', 12),
                text_color="red"
            )

    def confirm_delete(self):
        from tkinter import messagebox
        answer = messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить рецепт '{self.recipe.getName()}'?",
            parent=self
        )
        if answer:
            self.delete_recipe()

    def delete_recipe(self):
        try:
            db, cursor = get_database_connection()
            recipe_id = self.recipe.getId()

            # Сначала удаляем запись из БД
            cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            db.commit()

            # Закрываем изображение, если оно было загружено
            if hasattr(self, 'ctk_image'):
                self.image_label.configure(image=None)  # Отключаем изображение от виджета
                del self.ctk_image  # Удаляем ссылку на CTkImage

            # Удаляем файл изображения с повторными попытками
            image_path = os.path.join("recipe_images", self.recipe.getPicturePath())
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except PermissionError:
                    # Если файл занят, пробуем ещё раз после небольшой паузы
                    import time
                    time.sleep(0.5)
                    try:
                        os.remove(image_path)
                    except Exception as e:
                        print(f"Не удалось удалить изображение: {e}")
                        # Можно добавить очередь на удаление при следующем запуске

            messagebox.showinfo("Успех", "Рецепт успешно удален."
                                         " Чтобы увидеть изменения перезайдите на текущий экран", parent=self)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить рецепт: {str(e)}", parent=self)
        finally:
            close_database_connection(db)
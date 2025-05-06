import sqlite3
import os
import shutil
from classes import Recipe, User
from tkinter import messagebox
from PIL import ImageTk, Image
import customtkinter as ctk
from login.config import theme
import socket
import json
import datetime
import base64
import io

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432

# Функция для отправки запроса
def send_request(request):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_HOST, SERVER_PORT))
            s.sendall(json.dumps(request).encode('utf-8'))
            response = s.recv(10240).decode('utf-8')  # Увеличиваем размер буфера
            return json.loads(response)
    except (ConnectionError, json.JSONDecodeError) as e:
        print(f"Network error: {e}")
        return {"status": "error", "message": "Network error"}

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

# Функция обновления рецепта
def update_recipe(old_recipe, new_recipe, by_admin=False):
    try:
        image_data = None
        image_name = old_recipe.getPicturePath()
        if old_recipe.getPicturePath() != new_recipe.getPicturePath():
            image_path = new_recipe.getPicturePath()
            with open(image_path, 'rb') as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')
            image_name = os.path.basename(image_path)
        recipe_data = {
            "id": old_recipe.getId(),
            "author_name": new_recipe.getAuthor(),
            "recipe_name": new_recipe.getName(),
            "description": new_recipe.getDescription(),
            "cooking_time": new_recipe.getCookingTime(),
            "products": ', '.join(new_recipe.getProductList()),
            "image_name": image_name,
            "image_data": image_data,
            "old_image": old_recipe.getPicturePath()
        }
        response = send_request({
            "action": "update_recipe",
            "recipe_data": recipe_data,
            "by_admin": by_admin
        })
        return response.get("status") == "success"
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при обновлении рецепта: {str(e)}")
        return False

# Функция загрузки рецептов
def load_recipes(only_confirmed=True, limit=None, by_author=None, by_name=None, by_ingredients=None):
    response = send_request({
        "action": "load_recipes",
        "only_confirmed": only_confirmed,
        "limit": limit,
        "by_author": by_author,
        "by_name": by_name,
        "by_ingredients": by_ingredients
    })

    if response.get("status") == "success":
        recipes = []
        for recipe_data in response.get("recipes", []):
            try:
                recipes.append(Recipe(
                    id=recipe_data["id"],
                    author=recipe_data['author_name'],
                    name=recipe_data['recipe_name'],
                    description=recipe_data['description'],
                    picture_path=recipe_data['picture_path'],
                    cooking_time=recipe_data['cooking_time'],
                    product_list=[p.strip() for p in recipe_data['products'].split(',')],
                    confirmed=recipe_data['confirmed']
                ))
            except Exception as e:
                print(f"Error creating Recipe object: {e}")
                continue
        return recipes
    return []

# Функция для загрузки пользователей
def load_users():
    response = send_request({"action": "load_users"})
    if response.get("status") == "success":
        users = []
        for user_data in response.get("users", []):
            try:
                users.append(User(
                    id=user_data["id"],
                    username=user_data['username'],
                    password=user_data['password'],
                    admin=user_data['admin'],
                    authorized=user_data['authorized']
                ))
            except Exception as e:
                print(f"Error creating User object: {e}")
                continue
        return users
    return []

# Функция сохранения рецептов
def copy_image(source_path, destination_folder="recipe_images"):
    try:
        if not os.path.exists(source_path):
            print(f"Ошибка: файла {source_path} не существует")
            return None
        os.makedirs(destination_folder, exist_ok=True)
        filename = os.path.basename(source_path)
        base, ext = os.path.splitext(filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{base}_{timestamp}{ext}"
        unique_destination = os.path.join(destination_folder, unique_filename)
        shutil.copy2(source_path, unique_destination)
        return unique_destination
    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        return None

def save_recipe(recipe):
    try:
        image_path = recipe.getPicturePath()
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Файл изображения не найден: {image_path}")
        img = Image.open(image_path)
        max_size = (800, 800)
        img.thumbnail(max_size, Image.LANCZOS)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        recipe_data = {
            "author_name": recipe.getAuthor(),
            "recipe_name": recipe.getName(),
            "description": recipe.getDescription(),
            "cooking_time": recipe.getCookingTime(),
            "products": ', '.join(recipe.getProductList()),
            "image_name": os.path.basename(image_path),
            "image_data": image_data,
            "confirmed": recipe.getConfirmed()
        }
        response = send_request({
            "action": "save_recipe",
            "recipe_data": recipe_data
        })
        if response.get("status") == "success":
            return response.get("recipe_id")
        else:
            messagebox.showerror("Ошибка", response.get("message", "Неизвестная ошибка сервера"))
            return None
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при сохранении рецепта: {str(e)}")
        return None

def update_recipe_by_id(old_recipe, new_recipe, by_admin=False):
    response = send_request({
        "action": "update_recipe",
        "recipe_data": {
            "id": old_recipe.getId(),
            "author_name": new_recipe.getAuthor(),
            "recipe_name": new_recipe.getName(),
            "description": new_recipe.getDescription(),
            "cooking_time": new_recipe.getCookingTime(),
            "products": ', '.join(new_recipe.getProductList()),
            "image_name": os.path.basename(new_recipe.getPicturePath()),
            "image_data": None,
            "old_image": old_recipe.getPicturePath()
        },
        "by_admin": by_admin
    })
    return response.get("status") == "success"

# Функция удаления рецепта
def delete_recipe(recipe):
    response = send_request({
        "action": "delete_recipe",
        "recipe_id": recipe.getId()
    })
    return response.get("status") == "success"

# Функция для одобрения пользователя
def accept_user(user):
    response = send_request({
        "action": "activate_user",
        "user_id": user.getId()
    })
    return response.get("status") == "success"

# Функция для выдачи админки
def grant_admin_privileges(user):
    response = send_request({
        "action": "grant_admin_privileges",
        "user_id": user.getId()
    })
    return response.get("status") == "success"

def delete_user(user):
    response = send_request({
        "action": "delete_user",
        "user_id": user.getId()
    })
    return response.get("status") == "success"

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
            text=recipe.getName().capitalize(),
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
            fg_color="#db0404",
            hover_color="#910000",
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
        answer = messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить рецепт '{self.recipe.getName()}'?",
            parent=self
        )
        if answer:
            if delete_recipe(self.recipe):
                self.destroy()
                # Обновляем список рецептов в родительском окне
                if hasattr(self.main_program, 'user_profile_frame'):
                    self.main_program.user_profile_frame.display_recipes()
                elif hasattr(self.main_program, 'main_frame'):
                    self.main_program.main_frame.display_recipes()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить рецепт", parent=self)

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

            messagebox.showinfo("Успех", "Рецепт успешно удален.", parent=self)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить рецепт: {str(e)}", parent=self)
        finally:
            close_database_connection(db)

# Класс для карточки рецепта (для Администрации)
class AdminRecipeCard(ctk.CTkFrame):
    def __init__(self, master, recipe, main_program):
        super().__init__(
            master,
            fg_color=theme['recipe_card_fg_color'],
            corner_radius=10,
            border_width=1,
            width=1230,
            height=150
        )
        self.main_program = main_program
        self.recipe = recipe
        self.ctk_image = None  # Для хранения CTkImage

        # Заголовок (название рецепта)
        self.name_label = ctk.CTkLabel(
            master=self,
            text=recipe.getName(),
            font=("Aria", 14, "bold"),
            wraplength=180,
            text_color=theme['text_color'],
            height=40
        )
        self.name_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        # Название красного цвета, для не подтвержденного рецепта
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
        self.image_label.place(relx=0.01, rely=0.5, anchor='w')

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
        self.desc_label.place(rely=0.4, relx=0.2, anchor='w')

        # Кнопка "Удалить"
        self.delete_btn = ctk.CTkButton(
            master=self,
            text="Удалить",
            width=120,
            height=30,
            fg_color="#db0404",
            hover_color="#910000",
            text_color="white",
            command=self.confirm_delete
        )
        self.delete_btn.place(x=1100, y=40, anchor='w')

        # Кнопка "Редактировать"
        self.edit_btn = ctk.CTkButton(
            master=self,
            text="Редактировать",
            width=120,
            height=30,
            fg_color=theme['fg_color'],
            hover_color=theme['hover_color'],
            command=lambda: self.main_program.open_edit_recipe_frame(recipe)
        )
        self.edit_btn.place(x=1100, y=80, anchor='w')

        # Если рецепт не одобрен, то кнопка редактировать будет описана, как одобрить
        if not self.recipe.getConfirmed():
            self.edit_btn.configure(
                text="Одобрить",
                fg_color="#17ad03",
                hover_color="#0c5c02",
            )

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

            messagebox.showinfo("Успех", "Рецепт успешно удален.", parent=self)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить рецепт: {str(e)}", parent=self)
        finally:
            close_database_connection(db)
            # Обновляем список рецептов в программе после удаления
            self.main_program.main_frame.display_recipes()

class UserCard(ctk.CTkFrame):
    def __init__(self, master, user, main_program):
        super().__init__(
            master,
            fg_color=theme['recipe_card_fg_color'],
            corner_radius=10,
            border_width=1,
            width=1230,
            height=60
        )

        self.user = user
        self.main_program = main_program

        # Метка с логином аккаунта
        self.username_label = ctk.CTkLabel(
            master=self,
            text=self.user.getUsername(),
            text_color="green",
            font=("Century Gothic", 14, "bold"),
        )
        self.username_label.place(rely=0.5, relx=0.02,anchor="w")

        # Если пользователь не подтвержден, то делаем его логин красным
        if not self.user.isAuthorized():
            self.username_label.configure(text_color="red")

        # Если пользователь является админом, то его логин синий
        if self.user.isAdmin():
            self.username_label.configure(text_color="blue")

        # Если этот пользователь вы сам, то ваш ник будет золотым
        if self.main_program.user.getUsername() == self.user.getUsername():
            self.username_label.configure(text_color="gold")

        # Кнопка удаления пользователя
        self.delete_user_button = ctk.CTkButton(
            master=self,
            text="Удалить",
            corner_radius=6,
            width=100,
            fg_color="#db0404",
            hover_color="#910000",
            command=self.confirm_user_delete
        )
        self.delete_user_button.place(rely=0.5, relx=0.9,anchor="w")

        # Кнопка одобрения для не подтвержденных пользователей
        if not self.user.isAuthorized():
            self.accept_user_button = ctk.CTkButton(
                master=self,
                text="Одобрить",
                corner_radius=6,
                width=100,
                fg_color="#17ad03",
                hover_color="#0c5c02",
                command=self.confirm_user_confirm
            )
            self.accept_user_button.place(rely=0.5, relx=0.8,anchor="w")

        # Если пользователь не является админом, то появляется кнопка для того, чтобы сделать его админом
        if not self.user.isAdmin():
            self.set_admin_button = ctk.CTkButton(
                master=self,
                text="Сделать админом",
                corner_radius=6,
                width=200,
                command=self.confirm_user_admin
            )
            self.set_admin_button.place(rely=0.5, relx=0.6,anchor="w")

    # Метод для верификации пользователя
    def confirm_user_confirm(self):
        answer = messagebox.askyesno(
            "Подтверждение верификации",
            f"Вы уверены, что хотите подтвердить пользователя '{self.user.getUsername()}'?",
            parent=self
        )

        if answer:
            accept_user(self.user)
            self.main_program.main_frame.display_users()

    # Метод для выдачи админки
    def confirm_user_admin(self):
        answer = messagebox.askyesno(
            "Подтверждение админки",
            f"Вы уверены, что хотите выдать пользователю '{self.user.getUsername()}' права администратора?",
        )
        if answer:
            grant_admin_privileges(self.user)
            self.main_program.main_frame.display_users()

    # Метод дял подтверждения удаления пользователя
    def confirm_user_delete(self):
        answer = messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить пользователя '{self.user.getUsername()}'?",
            parent=self
        )
        if answer:
            delete_user(self.user)
            self.main_program.main_frame.display_users()
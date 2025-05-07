import sqlite3
import os
import shutil
from classes import Recipe, User
from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
from login.config import theme
import socket
import json
import datetime
import base64
import io

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 65432

def send_request(request):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((SERVER_HOST, SERVER_PORT))
            request_data = json.dumps(request).encode('utf-8')
            s.sendall(request_data)
            response = ""
            while True:
                chunk = s.recv(4096).decode('utf-8')
                if not chunk:
                    break
                response += chunk
                if response.endswith('}'):
                    break
            return json.loads(response)
    except (ConnectionError, json.JSONDecodeError) as e:
        print(f"Network error: {e}")
        return {"status": "error", "message": "Network error"}

def get_database_connection():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    return db, cursor

def close_database_connection(db):
    if db:
        db.close()

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
        os.makedirs("recipe_images", exist_ok=True)
        for recipe_data in response.get("recipes", []):
            try:
                picture_path = recipe_data['picture_path']
                if recipe_data.get('image_data'):
                    image_path = os.path.join("recipe_images", picture_path)
                    with open(image_path, 'wb') as img_file:
                        img_file.write(base64.b64decode(recipe_data['image_data']))
                recipes.append(Recipe(
                    id=recipe_data["id"],
                    author=recipe_data['author_name'],
                    name=recipe_data['recipe_name'],
                    description=recipe_data['description'],
                    picture_path=picture_path,
                    cooking_time=recipe_data['cooking_time'],
                    product_list=[p.strip() for p in recipe_data['products'].split(',') if p.strip()],
                    confirmed=recipe_data['confirmed']
                ))
            except Exception as e:
                print(f"Error processing recipe {recipe_data.get('recipe_name', 'unknown')}: {e}")
                continue
        return recipes
    return []

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

def delete_recipe(recipe):
    response = send_request({
        "action": "delete_recipe",
        "recipe_id": recipe.getId()
    })
    return response.get("status") == "success"

def accept_user(user):
    response = send_request({
        "action": "activate_user",
        "user_id": user.getId()
    })
    return response.get("status") == "success"

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
        self.ctk_image = None

        self.grid_columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(
            master=self,
            text=recipe.getName().capitalize(),
            font=("Arial", 14, "bold"),
            wraplength=180,
            text_color=theme['text_color'],
            height=40
        )
        self.name_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="n")

        if not recipe.getConfirmed():
            self.name_label.configure(text_color="red")

        self.image_label = ctk.CTkLabel(
            self,
            text="",
            width=180,
            height=120,
            fg_color="transparent",
            corner_radius=8
        )
        self.image_label.grid(row=1, column=0, padx=10, pady=5)

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

        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=3, column=0, pady=(5, 10))

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
                self.ctk_image = ctk.CTkImage(
                    light_image=Image.open(image_path),
                    dark_image=Image.open(image_path),
                    size=(180, 120)
                )
                self.image_label.configure(image=self.ctk_image, text="")
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
            cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            db.commit()
            if hasattr(self, 'ctk_image'):
                self.image_label.configure(image=None)
                del self.ctk_image
            image_path = os.path.join("recipe_images", self.recipe.getPicturePath())
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except PermissionError:
                    import time
                    time.sleep(0.5)
                    try:
                        os.remove(image_path)
                    except Exception as e:
                        print(f"Не удалось удалить изображение: {e}")
            messagebox.showinfo("Успех", "Рецепт успешно удален.", parent=self)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить рецепт: {str(e)}", parent=self)
        finally:
            close_database_connection(db)

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
        self.ctk_image = None

        self.name_label = ctk.CTkLabel(
            master=self,
            text=recipe.getName(),
            font=("Arial", 14, "bold"),
            wraplength=180,
            text_color=theme['text_color'],
            height=40
        )
        self.name_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        if not recipe.getConfirmed():
            self.name_label.configure(text_color="red")

        self.image_label = ctk.CTkLabel(
            self,
            text="",
            width=180,
            height=120,
            fg_color="transparent",
            corner_radius=8
        )
        self.image_label.place(relx=0.01, rely=0.5, anchor='w')

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
                self.ctk_image = ctk.CTkImage(
                    light_image=Image.open(image_path),
                    dark_image=Image.open(image_path),
                    size=(180, 120)
                )
                self.image_label.configure(image=self.ctk_image, text="")
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
            cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            db.commit()
            if hasattr(self, 'ctk_image'):
                self.image_label.configure(image=None)
                del self.ctk_image
            image_path = os.path.join("recipe_images", self.recipe.getPicturePath())
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except PermissionError:
                    import time
                    time.sleep(0.5)
                    try:
                        os.remove(image_path)
                    except Exception as e:
                        print(f"Не удалось удалить изображение: {e}")
            messagebox.showinfo("Успех", "Рецепт успешно удален.", parent=self)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить рецепт: {str(e)}", parent=self)
        finally:
            close_database_connection(db)
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

        self.username_label = ctk.CTkLabel(
            master=self,
            text=user.getUsername(),
            text_color="green",
            font=("Century Gothic", 14, "bold"),
        )
        self.username_label.place(rely=0.5, relx=0.02, anchor="w")

        if not user.isAuthorized():
            self.username_label.configure(text_color="red")
        if user.isAdmin():
            self.username_label.configure(text_color="blue")
        if self.main_program.user.getUsername() == user.getUsername():
            self.username_label.configure(text_color="gold")

        self.delete_user_button = ctk.CTkButton(
            master=self,
            text="Удалить",
            corner_radius=6,
            width=100,
            fg_color="#db0404",
            hover_color="#910000",
            command=self.confirm_user_delete
        )
        self.delete_user_button.place(rely=0.5, relx=0.9, anchor="w")

        if not user.isAuthorized():
            self.accept_user_button = ctk.CTkButton(
                master=self,
                text="Одобрить",
                corner_radius=6,
                width=100,
                fg_color="#17ad03",
                hover_color="#0c5c02",
                command=self.confirm_user_confirm
            )
            self.accept_user_button.place(rely=0.5, relx=0.8, anchor="w")

        if not user.isAdmin():
            self.set_admin_button = ctk.CTkButton(
                master=self,
                text="Сделать админом",
                corner_radius=6,
                width=200,
                command=self.confirm_user_admin
            )
            self.set_admin_button.place(rely=0.5, relx=0.6, anchor="w")

    def confirm_user_confirm(self):
        answer = messagebox.askyesno(
            "Подтверждение верификации",
            f"Вы уверены, что хотите подтвердить пользователя '{self.user.getUsername()}'?",
            parent=self
        )
        if answer:
            accept_user(self.user)
            self.main_program.main_frame.display_users()

    def confirm_user_admin(self):
        answer = messagebox.askyesno(
            "Подтверждение админки",
            f"Вы уверены, что хотите выдать пользователю '{self.user.getUsername()}' права администратора?",
        )
        if answer:
            grant_admin_privileges(self.user)
            self.main_program.main_frame.display_users()

    def confirm_user_delete(self):
        answer = messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить пользователя '{self.user.getUsername()}'?",
            parent=self
        )
        if answer:
            delete_user(self.user)
            self.main_program.main_frame.display_users()
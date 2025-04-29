import customtkinter as ctk
from customtkinter import CTkLabel
from login.config import theme
from tkinter import messagebox
from tkinter import filedialog
from classes import Recipe, RecipeCard
from PIL import Image
from functions import save_recipe, load_recipes

# Класс основного фрейма приложения
class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_main_frame()

    # Функция для отрисовки основного фрейма
    def setup_main_frame(self):
        # Create login frame
        self.main_frame = ctk.CTkFrame(master=self, width=1270, height=150)
        self.main_frame.place(relx=0.5, rely=0.12, anchor=ctk.CENTER)

        # top text
        self.text = CTkLabel(
            master=self.main_frame,
            text=self.master.user.getUsername(),
            font=('Times New Roman', 12)
        )
        self.text.place(x=90, y=45)

        # Exit button
        self.exit_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Закрыть",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.close_program
        )
        self.exit_button.place(x=1160, y=10)

        # Search entry
        self.search_entry = ctk.CTkEntry(
            master=self.main_frame,
            fg_color="white",
            corner_radius=6,
            text_color="black",
            width=800,
            height=40,
            font=('Century Gothic', 16)
        )
        self.search_entry.place(relx=0.12, y=60)

        # Search button
        self.search_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            height=40,
            text="Поиск",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
        )
        self.search_button.place(x=980, y=60)

        # Add recipe button
        self.add_recipe_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Добавить рецепт",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.master.open_add_recipe_frame
        )
        self.add_recipe_button.place(x=10, y=10)

        # Загружаем рецепты
        self.recipes = load_recipes()

        # Создаем фрейм для отображения карточек рецептов
        self.recipes_container = ctk.CTkScrollableFrame(
            master=self,
            width=1200,
            height=500,
            fg_color="transparent"
        )
        self.recipes_container.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

        # Отображаем рецепты
        self.display_recipes()

    # Функция для закрытия программы
    def close_program(self):
        self.master.destroy()

    # Метод отображения рецептов
    def display_recipes(self):
        # Очищаем контейнер перед добавлением новых карточек
        for widget in self.recipes_container.winfo_children():
            widget.destroy()

        # Создаем карточки для каждого рецепта
        for i, recipe in enumerate(self.recipes):
            card = RecipeCard(
                master=self.recipes_container,
                recipe=recipe,
                main_program=self.master
            )
            card.grid(row=i//3, column=i%3, padx=10, pady=10)

class AddRecipeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.setup_add_recipe_frame()

    def setup_add_recipe_frame(self):
        # Create recipe frame
        self.add_recipe_frame = ctk.CTkFrame(master=self, width=1270, height=50)
        self.add_recipe_frame.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        # top text
        self.text = CTkLabel(
            master=self.add_recipe_frame,
            text="Добавление рецепта",
            font=('Century Gothic', 36),
            text_color=theme['text_color']
        )
        self.text.place(relx=0.35, rely=0)

        # Кнопка возврата к основному фрейму
        self.back_to_main = ctk.CTkButton(
            master=self.add_recipe_frame,
            width=100,
            text="Назад",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_to_main.place(x=10, y=10)

        self.recipe_data_frame = ctk.CTkFrame(
            master=self,
            width=1270,
            height=620
        )
        self.recipe_data_frame.place(relx=0.005, y=70)

        # Поле ввода названия рецепта
        self.recipe_name_entry = ctk.CTkEntry(
            master=self.recipe_data_frame,
            width=200,
            placeholder_text="Название рецепта",
            font=('Century Gothic', 12),
            fg_color=theme['textbox_bg_color'],
            border_width=0
        )
        self.recipe_name_entry.place(x=25, y=10)

        # Поле ввода времени приготовления
        self.recipe_cocking_time_entry = ctk.CTkEntry(
            master=self.recipe_data_frame,
            width=200,
            placeholder_text="Время приготовления (мин)",
            font=('Century Gothic', 12),
            fg_color=theme['textbox_bg_color'],
            border_width=0
        )
        self.recipe_cocking_time_entry.place(x=25, y=50)

        # метка продуктов
        CTkLabel(
            master=self.recipe_data_frame,
            text="Продкуты: ",
            font=('Century Gothic', 16),
        ).place(x=30, y=90)

        # поле для ввода продуктов для рецепта
        self.product_textbox = ctk.CTkTextbox(
            master=self.recipe_data_frame,
            font=('Century Gothic', 12),
            corner_radius=12,
            width=200,
            height=100,
            fg_color=theme['textbox_bg_color']
        )
        self.product_textbox.place(x=25, y=130)

        # Фрейм для изображения блюда
        self.recipe_photo_frame = ctk.CTkFrame(
            master=self.recipe_data_frame,
        )
        self.recipe_photo_frame.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        self.load_image_button = ctk.CTkButton(
            master=self.recipe_data_frame,
            fg_color=theme['fg_color'],
            hover_color=theme['hover_color'],
            font=('Century Gothic', 24),
            text="Загрузить изображение",
            command=self.load_image_dialog
        )
        self.load_image_button.place(relx=0.7, y=10)

        # метка описания
        CTkLabel(
            master=self.recipe_data_frame,
            text="Описание: ",
            font=('Century Gothic', 16),
        ).place(x=30, y=260)

        # поле для ввода описания рецепта
        self.description_textbox = ctk.CTkTextbox(
            master=self.recipe_data_frame,
            font=('Century Gothic', 12),
            corner_radius=12,
            width=1220,
            height=240,
            fg_color=theme['textbox_bg_color']
        )
        self.description_textbox.place(relx=0.5, y=430, anchor=ctk.CENTER)

        # кнопка подтверждения добавления рецепта
        self.send_recipe_button = ctk.CTkButton(
            master=self.recipe_data_frame,
            text="Отправить",
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            font=('Century Gothic', 24),
            command=self.send_recipe
        )
        self.send_recipe_button.place(relx=0.87, y=550)

    # Метод отправки рецепта
    def send_recipe(self):
        name = self.recipe_name_entry.get().strip()
        try:
            cocking_time = int(self.recipe_cocking_time_entry.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Время приготовления должно быть целым числом")

        ingredients = self.product_textbox.get('1.0', 'end').strip()
        description = self.description_textbox.get('1.0', 'end').strip()
        try:
            picture_path = self.selected_image_path
        except:
            messagebox.showerror("Ошибка", "Выберите картинку для рецепта")

        if name and cocking_time and ingredients and description and picture_path:
            ingredients = [i.strip().lower() for i in ingredients.split(',')]
            recipe = Recipe(self.master.user.getUsername() ,name, description, picture_path, cocking_time, ingredients)

            # Это для тестирования
            print(f"Название рецепта: {recipe.getName()}")
            print(f"Время приготовления: {recipe.getCookingTime()}")
            print(f"Описание: {recipe.getDescription()}")
            print(f"Список продуктов: {recipe.getProductList()}")
            print(f"Подтвержден: {recipe.getConfirmed()}")
            print(f"Путь к изображению: {recipe.getPicturePath()}")
            print("Автор ", recipe.getAuthor())

            # Сохраняем рецепт
            save_recipe(recipe)

            self.master.open_main_frame()

            return
        else:
            messagebox.showerror("Ошибка", "Вы не заполнили все поля")

        print("Вы отправили рецепт")

    def load_image_dialog(self):
        picture_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Изображения", "*.png *.jpg *.jpeg"), ("Все файлы", "*.*")]
        )
        if picture_path:
            print(f"Вы выбрали картинку на пути: {picture_path}")
            try:
                # Загружаем картинку с помощью Pillow
                original_image = Image.open(picture_path)

                # Получаем размер фрейма для изображения
                frame_width = self.recipe_photo_frame.winfo_width()
                frame_height = self.recipe_photo_frame.winfo_height()

                # Масштабируем изображенияе с сохранением пропорций
                image_ratio = original_image.width / original_image.height
                frame_ratio = frame_width / frame_height

                if frame_ratio > image_ratio:
                    # Подгоняем по высоте
                    new_height = frame_height
                    new_width = int(new_height * image_ratio)
                else:
                    # Подгоняем по ширине
                    new_width = frame_width
                    new_height = int(new_width / image_ratio)

                resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

                # Конвертируем для CTkImage
                ctk_image = ctk.CTkImage(
                    light_image=resized_image,
                    dark_image=resized_image,
                    size=(new_width, new_height)
                )

                for widget in self.recipe_photo_frame.winfo_children():
                    widget.destroy()

                # Создаем Label для отображения изображения
                image_label = ctk.CTkLabel(
                    self.recipe_photo_frame,
                    image=ctk_image,
                    text=""
                )
                image_label.pack(expand=True)

                # Сохраняем путь к изображению для следующей отправки
                self.selected_image_path = picture_path

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")
            return
        else:
            return

class ShowRecipeFrame(ctk.CTkFrame):
    def __init__(self, master, recipe):
        super().__init__(master)

        self.master = master
        self.recipe = recipe

        self.setup_show_recipe_frame()

    def setup_show_recipe_frame(self):
        # Основной фрейм
        self.show_recipe_frame = ctk.CTkFrame(master=self, width=1270, height=50)
        self.show_recipe_frame.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)

        # Кнопка возврата к основному фрейму
        self.back_to_main = ctk.CTkButton(
            master=self.show_recipe_frame,
            width=100,
            text="Назад",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_to_main.place(x=10, y=10)

        # Метка с названием рецепта
        CTkLabel(
            master=self.show_recipe_frame,
            text=f"{self.recipe.getName()} by {self.recipe.getAuthor()}",
            font=('Century Gothic', 24, 'bold'),
        ).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Фрейм для картинки рецепта
        self.recipe_image_frame = ctk.CTkFrame(
            master=self,
            fg_color="white",
        )
        self.recipe_image_frame.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)

        # Метка для ингредиентов
        CTkLabel(
            master=self,
            text="Ингредиенты:",
            font=('Century Gothic', 24, 'bold'),
        ).place(relx=0.08, rely=0.15, anchor=ctk.CENTER)

        start_y = 130

        # Создаем метку для каждого ингредиента
        for ingredient in self.recipe.getProductList():
            CTkLabel(
                master=self,
                text=ingredient,
                font=('Century Gothic', 20, 'bold'),
            ).place(relx=0.015, y=start_y)

            start_y += 25

        # Фрейм для описания рецепта
import customtkinter as ctk
from customtkinter import CTkLabel
from login.config import theme

# Класс основного фрейма приложения
class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_main_frame()

    # Функция для отрисовки основного фрейма
    def setup_main_frame(self):
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

        # Кнопка выхода из аккаунта
        self.change_account_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Сменить аккаунт",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.change_account
        )
        self.change_account_button.place(x=10, y=10)

        self.open_user_control_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Пользователи",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.master.open_user_control_frame
        )
        self.open_user_control_button.place(relx=0.2, y=10)

        self.open_recipe_control_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Публикации",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.master.open_recipe_control_frame
        )
        self.open_recipe_control_button.place(relx=0.5, y=10)

    # Функция для закрытия программы
    def close_program(self):
        self.master.destroy()

    # Функция для выхода к окну авторизации
    def change_account(self):
        print("Вы попытались сменить аккаунт")

class UserControlFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.setup_user_check_frame()

    def setup_user_check_frame(self):
        self.search_info_label = CTkLabel(
            master=self.master,
            text="Окно управления пользователями",
            font=('Century Gothic', 36),
        )
        self.search_info_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

class RecipeControlFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.setup_recipe_check_frame()

    def setup_recipe_check_frame(self):
        self.search_info_label = CTkLabel(
            master=self.master,
            text="Окно управления рецептами",
            font=('Century Gothic', 36),
        )
        self.search_info_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
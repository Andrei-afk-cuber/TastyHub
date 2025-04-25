import customtkinter as ctk
from customtkinter import CTkLabel
from .functions import toggle_password, check_login, register_user
from .config import theme
from tkinter import messagebox

# Класс основного фрейма приложения
class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_login_frame()

    # Функция для отрисовки основного фрейма
    def setup_login_frame(self):
        # Create login frame
        self.login_frame = ctk.CTkFrame(master=self, width=320, height=380)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # top text
        self.text = CTkLabel(
            master=self.login_frame,
            text="TastyHub",
            font=('Century Gothic', 32)
        )
        self.text.place(x=90, y=45)

        self.error_label = ctk.CTkLabel(
            master=self.login_frame,
            text="",
            font=('Century Gothic', 12),
            text_color="red",
        )
        self.error_label.place(x=70, y=80)

        # Username entry block
        self.u_block = ctk.CTkEntry(
            master=self.login_frame,
            width=220,
            placeholder_text="Username",
        )
        self.u_block.place(x=50, y=110)

        # Password entry block
        self.show_password_var = ctk.BooleanVar()
        self.p_block = ctk.CTkEntry(
            master=self.login_frame,
            width=220,
            placeholder_text="Password",
            show="*"
        )
        self.p_block.place(x=50, y=150)

        # checkbox for showing password
        self.show_password = ctk.CTkCheckBox(
            master=self.login_frame,
            text="Show Password",
            font=('Century Gothic', 12),
            command=lambda: toggle_password(self.p_block, self.show_password_var),  # ченкуть зачем тут лямбда
            variable=self.show_password_var,
            fg_color=theme['fg_color'],
            hover_color=theme['hover_color'],
        )
        self.show_password.place(x=50, y=190)

        # Login button
        self.login_button = ctk.CTkButton(
            master=self.login_frame,
            width=100,
            text="Login",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.check_login_credentials,
        )
        self.login_button.place(x=110, y=230)

        # Register button
        self.register_button = ctk.CTkButton(
            master=self.login_frame,
            width=100,
            text="Register",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.master.open_register_frame
        )
        self.register_button.place(x=110, y=270)

    # Функция для проверки пароля и логина
    def check_login_credentials(self):
        # Получаем из полей ввода логин и пароль
        username = self.u_block.get()
        password = self.p_block.get()

        # Вызов функции check_login
        user = check_login(username, password)

        # Если пользователь был успешно создан
        if user:
            # Успешный логин
            print("Login Successful")
            self.master.open_main_program(user)
        else:
            # Неуспешный логин
            self.error_label.configure(text="Неверный логин или пароль")

# Класс фрейма регистрации
class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_register_frame()

    # Метод отрисовки фрейма регистрации
    def setup_register_frame(self):
        self.master.change_title("Register")
        # Create the registration frame
        self.registration_frame = ctk.CTkFrame(
            master=self,
            width=320,
            height=380
        )
        self.registration_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Top text
        self.text = CTkLabel(
            master=self.registration_frame,
            text="Welcome to our \nfriendly family",
            font=('Century Gothic', 25)
        )
        self.text.place(x=55, y=25)

        self.back_button = ctk.CTkButton(
            master=self,
            width=30,
            height=30,
            text="Back",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.master.open_main_frame
        )
        self.back_button.place(x=10, y=10)

        # Entry fields for registration form
        self.username_entry = ctk.CTkEntry(
            master=self.registration_frame,
            width=220,
            placeholder_text="Name",
        )
        self.username_entry.place(x=50, y=100)

        self.show_password_var = ctk.BooleanVar()
        self.p_block = ctk.CTkEntry(
            master=self.registration_frame,
            width=220,
            placeholder_text="Password",
            show="*"
        )
        self.p_block.place(x=50, y=140)

        # checkbox for showing password
        self.show_password = ctk.CTkCheckBox(
            master=self.registration_frame,
            text="Show Password",
            font=('Century Gothic', 12),
            command=lambda: toggle_password(self.p_block, self.show_password_var),  # ченкуть зачем тут лямбда
            variable=self.show_password_var,
            fg_color=theme['fg_color'],
            hover_color=theme['hover_color'],
        )
        self.show_password.place(x=50, y=190)

        self.register_button = ctk.CTkButton(
            master=self.registration_frame,
            width=100,
            text="Register",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color'],
            command=self.new_user_data
        )
        self.register_button.place(x=110, y=340)

    # Метод для регистрации нового пользователя
    def new_user_data(self):
        username = self.username_entry.get()
        password = self.p_block.get()

        if not username or not password:
            print("Please enter both username and password")
            messagebox.showerror("Error", "Please enter both username and password")
            return

        if register_user(username, password):
            # Registration successful
            print("Registration Successful")
            messagebox.showinfo("Success", "Registration Successful")
            self.registration_frame.place_forget()
            self.master.open_main_frame()
            return
        else:
            # Handle the case where the username or email is already taken
            print("Username or password is already in use")
            messagebox.showerror("Error", "Username or password is already in use")
            return

# Класс фрейма после авторизации
class LoggedInFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.setup_logged_in_frame()

    def setup_logged_in_frame(self):
        self.master.change_geometry("1280x720")
        pass
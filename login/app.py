import customtkinter as tk
from .frames import MainFrame, RegistrationFrame

# Основное окно приложения
class MainApp(tk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(f"600x400")   # Standard size 600x400
        self.title("Sign into your account")
        self.iconbitmap("images/icon.ico")
        # Create the main frame
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.frames = {}

    # Функция для изменения геометрии
    def change_geometry(self, new_geometry):
        # Change the window geometry
        self.geometry(new_geometry)

    # Функция для изменения заголовка окна
    def change_title(self, new_title):
        # Change the window title
        self.title(new_title)

    # Функция создания фрейма регистрации
    def open_register_frame(self):
        # Уничтожаем основной фрейм и отрисовываем фрейм регистрации
        self.main_frame.destroy()
        # Запускаем фрейм регистрации
        self.register_frame = RegistrationFrame(self)
        self.frames['register_frame'] = self.register_frame
        self.register_frame.pack(expand=True, fill="both")

    # Открываем основной фрейм
    def open_main_frame(self):
        self.destroy_all_frames()
        self.change_title("Sign into your account")
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    # Функция для открытия фрейма после аутентификации
    def open_loggedin_frame(self):
        # Уничтожаем основной фрейм
        self.main_frame.destroy()

    def destroy_all_frames(self):
        # Удаляем все фреймы, которые есть в словаре
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}
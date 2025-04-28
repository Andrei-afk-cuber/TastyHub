import customtkinter as ctk
from admin_frames import MainFrame, UserControlFrame, RecipeControlFrame
from classes import User

# Основное окно приложения
class MainApp(ctk.CTk):
    def __init__(self, user=User("test_admin", 0000, True)):
        super().__init__()

        self.user = user

        self.geometry(f"1280x720+100+100")   # Standard size 600x400
        self.title("TastyHub Admin Controller")
        self.iconbitmap("images/icon.ico")
        # Create the main frame
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.frames = {}

    # Открываем основной фрейм
    def open_main_frame(self):
        self.destroy_all_frames()
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    # Метод открытия фрейма управления пользователями
    def open_user_control_frame(self):
        # Удаляем основной фрейм
        self.main_frame.destroy()
        # Открываем фрейм контроля пользователей
        self.user_control_frame = UserControlFrame(self)
        self.frames['user_control_frame'] = self.user_control_frame
        self.user_control_frame.pack(fill="both", expand=True)

    # Метод открытия фрейма управления рецептами
    def open_recipe_control_frame(self):
        # Удаляем основной фрейм
        self.main_frame.destroy()
        # Открываем фрейм управления рецептами
        self.recipe_control_frame = RecipeControlFrame(self)
        self.frames['recipe_control_frame'] = self.recipe_control_frame
        self.recipe_control_frame.pack(fill="both", expand=True)

    # Функция для открытия окна регистрации
    def open_register_program(self):
        pass

    # Функция удаления всех фреймов
    def destroy_all_frames(self):
        # Удаляем все фреймы, которые есть в словаре
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}


"""
Только для тестирования
"""
# MainApp().mainloop()
import customtkinter as ctk
from user_frames import MainFrame, AddRecipeFrame, ShowRecipeFrame, UserProfileFrame
from classes import User

# Основное окно приложения
class MainApp(ctk.CTk):
    def __init__(self, user=User("test_user", 0000, False)):
        super().__init__()

        self.user = user

        self.geometry(f"1280x720+100+100")   # Standard size 600x400
        self.title("TastyHub")
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

    # Метод открытия фрейма добавления рецепта
    def open_add_recipe_frame(self):
        # Удаляем основной ферйм
        self.main_frame.destroy()
        # Открываем фрейм добавления рецепта
        self.add_recipe_frame = AddRecipeFrame(self)
        self.frames['add_recipe_frame'] = self.add_recipe_frame
        self.add_recipe_frame.pack(fill="both", expand=True)

    # Метод открытия фрейма для просмотра данных о рецепте
    def open_show_recipe_frame(self, recipe):
        # Удаляем основной фрейм
        self.main_frame.destroy()
        # Открываем фрейм просмотра рецепта
        self.show_recipe_frame = ShowRecipeFrame(self, recipe)
        self.frames['show_recipe_frame'] = self.show_recipe_frame
        self.show_recipe_frame.pack(fill="both", expand=True)

    # Метод открытия фрейма для просмотра профиля
    def open_user_profile_frame(self):
        # Удаляем основной фрейм
        self.main_frame.destroy()
        # Открываем фрейм просмотра рецепта
        self.user_profile_frame = UserProfileFrame(self)
        self.frames['user_profile_frame'] = self.user_profile_frame
        self.user_profile_frame.pack(fill="both", expand=True)

    # Функция удаления всех фреймов
    def destroy_all_frames(self):
        # Удаляем все фреймы, которые есть в словаре
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}

# MainApp().mainloop()
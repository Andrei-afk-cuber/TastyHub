import customtkinter as ctk
from frames import MainFrame
# Основное окно приложения
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

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
        self.change_title("Sign into your account")
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    def destroy_all_frames(self):
        # Удаляем все фреймы, которые есть в словаре
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}

MainApp().mainloop()
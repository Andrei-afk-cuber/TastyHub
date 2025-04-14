import customtkinter as ctk
from customtkinter import CTkLabel
from login.config import theme
from tkinter import messagebox

# Класс основного фрейма приложения
class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_main_frame()

    # Функция для отрисовки основного фрейма
    def setup_main_frame(self):
        # Create login frame
        self.main_frame = ctk.CTkFrame(master=self, width=1270, height=380)
        self.main_frame.place(relx=0.5, rely=0.27, anchor=ctk.CENTER)

        # top text
        """self.text = CTkLabel(
            master=self.main_frame,
            text="TastyHub",
            font=('Century Gothic', 32)
        )
        self.text.place(x=90, y=45)"""

        # Exit button
        self.exit_button = ctk.CTkButton(
            master=self.main_frame,
            width=100,
            text="Close",
            corner_radius=6,
            fg_color=theme['fg_color'],
            text_color=theme['text_color'],
            hover_color=theme['hover_color']
        )
        self.exit_button.place(x=10, y=1100)

        self.btn = ctk.CTkButton()
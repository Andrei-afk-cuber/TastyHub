import customtkinter as ctk

class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        ctk.set_appearance_mode("Dark")
        self.root.title("TastyHub")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.iconbitmap("images/icon.ico")

        self.root.mainloop()

MainWindow()
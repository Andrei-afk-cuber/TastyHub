import customtkinter as tk
from .frames import MainFrame, RegistrationFrame

class MainApp(tk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(f"600x400")   # Standard size 600x400
        self.title("Sign into your account")
        # Create the main frame
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        self.frames = {}

    def change_geometry(self, new_geometry):
        # Change the window geometry
        self.geometry(new_geometry)

    def change_title(self, new_title):
        # Change the window title
        self.title(new_title)

    def open_register_frame(self):
        # Destroy the Main frame and open the Register Frame
        self.main_frame.destroy()
        # Start registration frame
        self.register_frame = RegistrationFrame(self)
        self.frames['register_frame'] = self.register_frame
        self.register_frame.pack(expand=True, fill="both")

    def open_main_frame(self):
        self.destroy_all_frames()
        self.change_title("Sign into your account")
        self.main_frame = MainFrame(self)
        self.main_frame.pack(fill="both", expand=True)

    def open_loggedin_frame(self):
        # Destroy the Main frame and open the Register frame
        self.main_frame.destroy()

    def destroy_all_frames(self):
        # Destroy all frames in the dictionary
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}
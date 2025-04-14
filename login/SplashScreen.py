import customtkinter as ctk
from tkinter import Label
from PIL import Image, ImageTk, ImageSequence

class SplashScreen:
    def __init__(self, root, duration):
        self.root = root
        self.gif_path = "../animations/welcome_video.gif"
        self.duration = duration

        # Создаем окно для стартового экрана
        self.splash = ctk.CTkToplevel(root)
        self.splash.overrideredirect(True)  # Убираем рамку окна
        self.splash.geometry("+{}+{}".format(
            root.winfo_screenwidth() // 2 - 200,  # Центрируем окно
            root.winfo_screenheight() // 2 - 200
        ))

        # Загружаем GIF
        self.gif = Image.open(self.gif_path)
        self.frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(self.gif)]

        # Отображаем первый кадр
        self.label = Label(self.splash, image=self.frames[0])
        self.label.pack()

        # Запускаем анимацию
        self.current_frame = 0
        self.animate()

        # Закрываем стартовый экран через указанное время
        self.splash.after(self.duration, self.close_splash)

    def animate(self):
        """Обновляет кадры GIF."""
        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 1
            self.label.config(image=self.frames[self.current_frame])
            self.splash.after(15, self.animate)  # Обновляем кадр каждые 30 мс (33 FPS)
        else:
            # Анимация завершена, закрываем стартовый экран
            self.close_splash()

    def close_splash(self):
        """Закрывает стартовый экран и запускает основную программу."""
        self.splash.destroy()
        self.root.deiconify()  # Показываем основное окно
        self.start_main_program()

    def start_main_program(self):
        """Запуск основной программы."""

# Создаем стартовый экран
splash = SplashScreen(root, 3000)  # 3000 мс = 3 секунды
root.mainloop()
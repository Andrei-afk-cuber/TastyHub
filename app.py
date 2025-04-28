import user_main_program as ump
import admin_main_program as amp
from login.app import LoginMainApp

# Создаем объект основной программы, чтобы передать её в окно регистрации
user_main_program = ump.MainApp
admin_main_program = amp.MainApp

if __name__ == '__main__':
    LoginMainApp(user_main_program, admin_main_program).mainloop()

"""
Это основной (связующий) файл программы
"""
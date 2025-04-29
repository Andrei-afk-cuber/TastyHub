import os
import shutil

def copy_image(source_path, destination_folder):
    try:
        # Проверяем существование исходного файла
        if not os.path.exists(source_path):
            print(f"Ошибка: фйла {source_path} не существует")
            return None

        # Проверяем что это файл (а не папка)
        if not os.path.isfile(source_path):
            print(f"Ошибка: {source_path} не является файлом")
            return None

        # Создаем целевую папку, если её нет
        os.makedirs(destination_folder, exist_ok=True)

        # Получаем имя файла из исходного пути
        file_name = os.path.basename(source_path)

        # Формируем полный путь назначения
        destination_path = os.path.join(destination_folder, file_name)

        # Копируем файл
        shutil.copy2(source_path, destination_path)
        print(f"Изображение скопировано в {destination_path}")
        return destination_path

    except Exception as e:
        print(f"Ошибка при копировании: {e}")
        return None

if __name__ == "__main__":
    source = "C:\\Users\\user\\Pictures\\Days Gone\\2023.10.21-23.00.38.png"
    destination = "recipe_images"

    copied_file = copy_image(source, destination)
    if copied_file:
        print(f"Успешно скопировано в {copied_file}")
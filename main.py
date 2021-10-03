import os
import sqlite3

# Константы и параметры конфигурации:
allow_formats = (".tif", ".jpeg", ".jpg")  # форматы изображений, с которыми будем работать
import_directory = input("Введите адрес папки с изображениями:")
output_directory = input("Введите адрес папки где будет хранится база данных и превью-картинки:")


def build_index_images(allow_formats, import_directory, output_directory):
    """ Находит в каталоге import_directory все файлы форматов allow_formats
    и строит индекс в папке output_directory"""
    database_path = str(output_directory + '/index.db')

    # если файл базы ранее уже создавался и лежит в папке, удалить его
    if os.path.isfile(database_path):
        os.remove(database_path)
        print("В указанной вами папке уже есть база данных, мы ее удалили, чтобы создать новый индекс")

    # Создание новой базы
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS images(
       image_id INT PRIMARY KEY,
       image_name TEXT,
       image_format TEXT,
       image_path TEXT,
       image_source INT,
       image_status INT,
       image_hash INT,
       image_height INT,
       image_width INT,
       image_preview_path TEXT,
       image_is_hash_changed INT,
       image_num_of_faces INT,
       image_num_of_persons INT);""")  # создаем таблицу информации об изображениях
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS faces(
        face_id INT PRIMARY KEY,
        image_id INT,
        face_coordinates TEXT,
        face_path TEXT,
        face_encoding TEXT,
        face_number_of_persons_match INT);""")  # создаем таблицу информации о найденных лицах
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS persons(
        person_id INT PRIMARY KEY,
        faces_id_list TEXT,
        person_name TEXT);""")  # создаем таблицу информации о персонах
    conn.commit()

    counter = 0
    for dirpath, dirnames, filenames in os.walk(import_directory):
        # перебор файлов в каталоге import_directory
        for filename in filenames:  # отбрасываем папки, оставляем только файлы
            if os.path.splitext(filename)[1] in allow_formats:  # отбрасывает файлы, отличные от allow_formats
                image_id = counter  # присваиваем номера изображений по порядку 0,1,2,3... и т.д.
                image_name = os.path.splitext(filename)[0]  # имя файла без расширения
                image_format = os.path.splitext(filename)[1]  # расширение файла, пример: ".jpg"
                image_path = os.path.join(dirpath, filename)  # полный путь файла с названием и форматом
                image_source = 0  # (0 - взят из базы, 1 - загружен вручную, 2 - из интернета)
                image_status = 0  # (0 - indexed, 1 - checked faces, 2 - checked persons, 3 - changed hash)
                image_hash = os.path.getsize(os.path.join(dirpath, filename))  # пока хэш - это размер файла

                image_info = (image_id, image_name, image_format, image_path, image_source, image_status, image_hash)
                print(image_info[3], " -> DONE")

                cur.execute("""INSERT INTO images(image_id, image_name, image_format, image_path, image_source, 
                    image_status, image_hash) VALUES(?, ?, ?, ?, ?, ?, ?);""", image_info)
                conn.commit()
                counter += 1
            else:
                print(os.path.join(dirpath, filename), " -> IGNORE")

    cur.execute("SELECT COUNT (*) FROM images")
    print("Количество проиндексированных изображений: ", cur.fetchone()[0])

    cur.execute("SELECT SUM(image_hash) FROM images")
    print("Суммарный вес нужных нам файлов в каталоге: ", round(cur.fetchone()[0]/1024/1024/1024, 2), "Гб")


def build_index_faces():
    pass


def build_index_persons():
    pass


if __name__ == '__main__':
    build_index_images(allow_formats, import_directory, output_directory)
    print("Индексация изображений прошла успешно")
    pass

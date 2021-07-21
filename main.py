import os
import sqlite3

# Константы и параметры конфигурации:
ALLOW_FORMATS = (".tif", ".jpeg", ".jpg")  # форматы файлов, которые мы ищем
images_folder_path = input("Введите адрес папки с изображениями:")
images_converted_folder_path = input("Введите адрес папки для сохранения уменьшенных копий картинок:")

def build_index_images(images_folder_path):
    """ Обходит папки и подпапки, находит файлы формата jpg, jpeg, tif, строит индекс:
    image_id - идентификатов по порядку (int)
    image_source_address - адрес и имя изначального файла (str)
    source - источник данных (int)
    (здесь source=0 - источник корневая папка. Будут еще: 1 - источник из интернета, 2 - подгрузка картинки вручную)

    После индексации идет стадия загрузки и обработки изображений, таблица пополнится столбцами:
    image_converted_address - адрес обработанной для распознавания картинки (str)
    (если на фото не найдены лица, то не хранить это фото, значит адрес будет пустой)
    image_status - статус картинки (str)
    (Если image_status = indexed - проиндексирована, converted - скачана, обработана и загружена)
    hash - хэш исходной картинки (str), чтобы следить не подменили ли картинку в базе
    hash_check_status - статус после проверки хэша файла (bool), True - не именился хэш, False - изменился и надо...
    ...заново распознать картинку.

    После распознавания таблица пополнится столбцами:
    is_any_faces - есть ли на фото лица (bool) True/False, True - нашлось хотя бы одно лицо, False - нет лиц
    num_of_faces - кол-во лиц, найденных на фото (int)
    """
    for dirpath, dirnames, filenames in os.walk(images_folder_path):
        # перебрать файлы
        for filename in filenames:  # перебирает только файлы, отбрасывая папки
            if os.path.splitext(filename)[1] in ALLOW_FORMATS:  # есть ли файлы выбранных нами форматов
                print(os.path.splitext(filename)) # выводит имя и формат файла в кортеж, пример: ('0-389255', '.tif')
                print(os.path.join(dirpath, filename))  # выводит абсолютный путь к файлу

    pass


def build_index_faces():
    pass


def build_index_persons():
    pass



if __name__ == '__main__':
    pass
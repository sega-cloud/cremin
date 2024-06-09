import os
import glob
import json
import tabula
import requests

# Функция для конвертации таблицы из PDF в json
def convert_pdf_table_to_json(pdf_file_path, page_number):
    # Извлечение таблицы с указанной страницы
    df = tabula.read_pdf(pdf_file_path, pages=page_number, multiple_tables=True)[0]
    # Преобразование DataFrame в JSON
    json_data = df.to_json(orient='records', force_ascii=False)
    return json_data

# Функция для отправки JSON на сервер с помощью POST-запроса
def send_json_to_server(json_data, url):
    # Отправка JSON на сервер
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    return response

# Путь к папке, где ожидается наличие файла
folder_path = '/Volumes/Update/ПДФ'
# Шаблон поиска для файлов PDF
pattern = '*.pdf'

# Поиск всех PDF-файлов в папке
pdf_files = glob.glob(os.path.join(folder_path, pattern))

# Проверка наличия PDF-файлов
if pdf_files:
    # Использование первого найденного PDF-файла
    pdf_path = pdf_files[0]
    page_number = 1  # Номер страницы с таблицей
    json_result = convert_pdf_table_to_json(pdf_path, page_number)
    print(json_result)

    # URL сервера, на который вы хотите отправить JSON
    server_url = 'https://cremin.ru/cr-system/scenario/socet'

    # Отправка JSON на сервер
    response = send_json_to_server(json_result, server_url)
if response.status_code == 200:
    print('JSON успешно отправлен')
    # Удаление файла после успешной отправки
    try:
        os.remove(pdf_path)
        print(f'Файл {pdf_path} был успешно удален')
    except OSError as e:
        print(f'Ошибка при удалении файла {pdf_path}: {e}')
else:
    print('Ошибка при отправке JSON:', response.status_code)

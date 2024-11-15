from datetime import datetime
import csv

def console_output():
    input_file = 'schedule.csv'
    output_file = 'output.txt'

    day_of_week = datetime.now().weekday()

    # Открываем CSV файл для чтения
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)  # Читаем заголовки (это первая строка)

        # Читаем первую строку данных
        first_row = next(reader)  # Это будет первая строка расписания (не заголовок)

        # Получаем содержимое для выбранного дня недели
        content = first_row[day_of_week]  # day_of_week - это индекс столбца

    # Записываем в новый текстовый файл
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(content.strip() + '\n')

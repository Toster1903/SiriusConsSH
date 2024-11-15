from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

def parsing():
    # Настройки для браузера
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.get("https://schedule.siriusuniversity.ru/")

    # Выбираем группу
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div").click()
    driver.find_element(By.XPATH, '//*[@id="searchListInput"]').send_keys('К0609-24')
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="searchList"]/li').click()
    time.sleep(2)

    # Находим таблицу с расписанием
    div = driver.find_element(By.CSS_SELECTOR, "div.max-h-rasp-table.overflow-auto.block")
    days = div.find_elements(By.CSS_SELECTOR, "table td")

    # Списки для хранения данных
    schedule_data = []

    # Обработка данных
    for element in days:
        if element.text == '':
            discipline = 'Окно'
            teacher = ''
            room = ''
        else:
            # Парсим предмет
            discipline = element.find_element(By.CSS_SELECTOR, "div.pr-2.pl-2.pb-2.font-bold.rasp-grid-min-discipline.text-xs").text
            
            # Парсим преподавателя
            try:
                teacher = element.find_element(By.CSS_SELECTOR, "span.line-clamp-2 span").text
            except:
                teacher = ''
            
            # Парсим аудиторию
            try:
                room = element.find_element(By.CSS_SELECTOR, "div.text-gray-500.flex span span").text
            except:
                room = ''
        
        # Добавляем данные для текущей ячейки в список
        schedule_data.append({
            'discipline': discipline,
            'teacher': teacher,
            'room': room
        })

    # Дни недели
    days_of_week = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']

    # Разбиваем данные на пары для каждого дня недели
    lessons_per_day = 7
    table_data = []

    # Заголовок для таблицы
    table_data.append(['№ пары'] + days_of_week)

    # Формируем строки для таблицы с добавлением информации о номере пары, дисциплине, преподавателе и аудитории
    for i in range(0, len(schedule_data), lessons_per_day):
        row = [i // lessons_per_day + 1]  # Номер пары
        for j in range(lessons_per_day):
            index = i + j
            if index < len(schedule_data):
                lesson = schedule_data[index]
                # Добавляем информацию о дисциплине, преподавателе и аудитории
                row.append(f"{lesson['discipline']}\n{lesson['teacher']}\n{lesson['room']}")
            else:
                row.append('')
        table_data.append(row)

    # Записываем данные в CSV
    with open('schedule.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table_data)

    driver.quit()

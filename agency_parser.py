from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import csv
import argparse
import re
import requests

parser = argparse.ArgumentParser(description='file to put ads')
parser.add_argument('--filename', type=str,help='file to put ads')
parser.add_argument('--startpage', type=int,help='file to put ads')
parser.add_argument('--endpage', type=int,help='file to put ads')
args = parser.parse_args()
filename = args.filename
startpage = args.startpage
endpage = args.endpage

PATH = "C:\\Users\\Computer\\Desktop\\chromedriver.exe"

driver = webdriver.Chrome(executable_path=PATH)

driver.get('http://www.all-agency.ru/')
list_of_hrefs = []
# Количество страниц с объявлениями
for i in range(startpage, endpage+1):
    r = requests.get(f'http://www.all-agency.ru/page/{i}/')
    if r.status_code == 404:
        continue
    driver.get(f'http://www.all-agency.ru/page/{i}/')
    posts = driver.find_elements_by_class_name('Post2')
    for post in posts:
        href = post.find_element_by_tag_name('a').get_attribute('href')
        list_of_hrefs.append(href)
        print(href)
    # Проходимся по ссылкам на объявления
    for href in list_of_hrefs:
        driver.get(href)
        header = driver.find_element_by_class_name('PostHead')
        name = header.find_element_by_tag_name('h1').text
        info = driver.find_element_by_class_name('PostContent').text

        # Отделяем кучу текста от основной информации
        splitted_info = info.split('Информация о компании:')[0].split('\n')
        
        # Заранее выставляем всем данным значение не указан что чтобы не прописывать else
        region, metro, address = 'Регион не указан', 'Метро не указано', 'Адрес не указан'
        email, phone, site = 'Почта не указана', 'Телефон не указан', 'Сайт не указан'

        # Ищем нужные нам данные по собранному тексту
        for data in splitted_info:
            if 'Регион:' in data:
                region = data
            elif 'Метро:' in data:
                metro = data
            elif 'Адрес:' in data:
                address = data
            elif 'E-mail:' in data:
                email = data
            elif 'Сайт:' in data or 'www' in data:
                site = data

            # Используется много regexp так как номера телефонов выглядят по разному
            elif 'Телефон:' in data or re.match(r'\d{3}-\d{3,4}', data) \
                or re.match(r'\d{1}-\d{3}-\d{3}-\d{2}-\d{2}', data) \
                or re.match(r'(\d{3})', data):
                phone = data

        # У некоторых объявлений нет дополнительной информации
        try:
            other_info = ' '.join(info.split('Информация о компании:')[1].split('\n'))
        except IndexError:
            print('Нет дополнительной информации')
            other_info = 'Нет дополнительной информации'
        with open(filename, 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Название', 'Регион', 'Метро', 'Адрес',
                             'Почта', 'Сайт', 'Телефон', 'Ссылка', 
                             'Дополнительная инофрмация'])
            writer.writerow([name, region, metro, 
                             address, email, site, 
                            phone, href, other_info])

    # Удаляем все ссылки с предыдущей страницы
    list_of_hrefs = []
driver.quit()


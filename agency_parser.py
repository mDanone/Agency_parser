from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import csv
import argparse

parser = argparse.ArgumentParser(description='file to put ads')
parser.add_argument('--filename', type=str,help='file to put ads')
args = parser.parse_args()
filename = args.filename

PATH = "C:\\Users\\Computer\\Desktop\\chromedriver.exe"

'''
   maininfo[0]: Регион, maininfo[1]: Метро
   maininfo[2]: Название организации, 
   maininfo[3]: Адрес, maininfo[4]: Телефон,
   maininfo[5]: Email, maininfo[6]: Сайт
'''

driver = webdriver.Chrome(executable_path=PATH)

driver.get('http://www.all-agency.ru/')
list_of_hrefs = []

for i in range(1, 162):
    driver.get('http://www.all-agency.ru/page/{}/'.format(i))
    posts = driver.find_elements_by_class_name('Post2')
    for post in posts:
        href = post.find_element_by_tag_name('a').get_attribute('href')
        list_of_hrefs.append(href)
        print(href)
    for href in list_of_hrefs:
        driver.get(href)
        header = driver.find_element_by_class_name('PostHead')
        name = header.find_element_by_tag_name('h1').text
        info = driver.find_element_by_class_name('PostContent').text
        splitted_info = info.split('Информация о компании:')[0].split('\n')
        region, metro, address = 'Не указано', 'Не указано', 'Не указано'
        email, phone, site = 'Не указано', 'Не указано', 'Не указано'
        for data in splitted_info:
            if 'Регион:' in data:
                region = data
            elif 'Метро:' in data:
                metro = data
            elif 'Адрес:' in data:
                address = data
            elif 'E-mail:' in data:
                email = data
            elif 'Сайт:' in data:
                site = data
            elif 'Телефон:' in data:
                phone = data
        # У некоторых объявлений нет дополнительной информации
        try:
            other_info = ' '.join(info.split('Информация о компании:')[1].split('\n'))
        except IndexError:
            print('Нет дополнительной информации')
            other_info = 'Нет дополнительной информации'
        with open(filename, 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([name, region, metro, 
                             address, email, site, 
                            phone, href, other_info])
        list_of_hrefs = []


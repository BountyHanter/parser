import csv
import json

import bs4
from bs4 import BeautifulSoup
import requests
import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime
import pandas as pd


"""url = 'https://market.dota2.net/?search=Feast%20of%20Abscession&sd=desc'

req = requests.get(url, headers=headers)
src = req.text"""
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36'
}

"""with open('index.html', 'w', encoding='utf-8') as file:
    file.write(src)"""

"""
all_links = soup.find(class_='market-items').find_all(class_='item')
all_full_links = []
for item in all_links:
    links = item.get('href')
    all_full_links.append('https://market.dota2.net'+links)
print(all_full_links)

with open('all_links.json', 'w') as file:
    json.dump(all_full_links, file, indent=4, ensure_ascii=False)
    """

with open(f'data/result.csv', 'a', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')

with open('all_links.json') as file:
    all_links = json.load(file)
count = 0
for link in all_links:
    count += 1
    if count == 1:
        with open(f'data/{count}.html', encoding='utf-8') as file:
            src = file.read()
        # Вообще нужно еще учесть то что может залезть комплект, учесть это нужно и не включать его в список
        url = 'https://market.dota2.net/item/2777687741-3104197121-Exalted%20Feast%20of%20Abscession/'

        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        price = soup.find(class_='ip-bestprice').text
        print(price)
        expansible = []
        element = soup.find(class_='expansible').find(style='color: #625e56;')
        if element is not None:  # это предотвращает ошибку если там чего то нет
            element = soup.find(class_='expansible').find(style='color: #625e56;').next_element.next_element.text
            if element is not None:
                expansible.append(element)
            element = soup.find(class_='expansible').find(style='color: #625e56;').next_element.next_element.next_element.next_element.text
            if element is not None:
                expansible.append(element)
        element = soup.find(class_='expansible').find(style='white-space: nowrap; margin: 10px')
        if element is not None:  # это предотвращает ошибку если нет рун
            element = soup.find(class_='expansible').find(style='white-space: nowrap; margin: 10px').find_all(
                style='vertical-align: top; display: inline-block; margin-left: 12px padding: 2px')
        print(expansible)
        runes = []
        if element is not None:
            for item in element:
                itm1 = item.find('span', style='font-size: 18px; white-space: normal; color: rgb(0, 0, 0)').text
                itm2 = item.find('span', style='font-size: 12px').text
                print(itm1, ', Тип: ', itm2)
                runes.append(itm1+', Тип: '+itm2)


        with open(f'data/result.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow((price,expansible,runes))
"""one = 'Цена'
two = 'Стили'
three = 'Руна/Тип руны'
with open(f'data/result.csv', 'a', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow((one,two,three))"""
import csv
import json
import os.path
import bs4
import psycopg2
from bs4 import BeautifulSoup
import requests
import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime
import pandas as pd
from config import password, db_name, user, host

def to_infinity():
    index = 0
    while True:
        yield index
        index += 1


class Parser:
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36'
    }

    def load_start_pages(self, headers=headers):
        """Загружаем страницы с товарами"""
        for i in to_infinity():
            start_url = f'https://market.dota2.net/?p={i + 1}&search=Feast%20of%20Abscession&sd=desc'
            req = requests.get(start_url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            all_items_in_page = soup.find(class_='market-items').find(class_='item')
            if all_items_in_page is not None:  # проверяем, если на странице есть товар то записываем его html код и идём на следующую страницу
                with open(f'index{i + 1}.html', 'w', encoding='utf-8') as file:
                    file.write(src)
            else:
                break

    def load_all_links_to_pages(self):
        """Загружаем все страницы товаров"""
        all_links_in_pages = []
        for i in to_infinity():
            file_path = f'index{i + 1}.html'
            if os.path.exists(file_path) is True:
                with open(f'index{i + 1}.html', encoding='utf-8') as file:
                    src = file.read()
                soup = BeautifulSoup(src, 'lxml')
                all_items_in_page = soup.find(class_='market-items').find_all(class_='item')
                for item in all_items_in_page:
                    links = item.get('href')
                    all_links_in_pages.append('https://market.dota2.net' + links)
            elif os.path.exists(file_path) is False:
                with open('all_links.json', 'a') as file:
                    json.dump(all_links_in_pages, file, indent=4, ensure_ascii=False)
                break

    def load_all_pages(self, headers=headers):
        """Сохраняем все html коды всех товаров"""
        with open('all_links.json') as file:
            all_links = json.load(file)
        counter = 1
        for item in all_links:
            url = item
            req = requests.get(url, headers=headers)
            src = req.text
            with open(f'data/{counter}.html', 'w', encoding='utf-8') as file:
                file.write(src)
            counter += 1
            print(counter, "сохранён")

    def information(self):
        """Вспомогательная функци чтобы посмотреть информацию о конкретном товаре"""
        print("Введите номер товара о котором ходтите получить информацию")
        count = input()
        with open(f'data/{count}.html', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        price = soup.find(class_='ip-bestprice').text
        print(price)
        expansible = []
        element = soup.find(class_='expansible').find(style='color: #625e56;')
        if element is not None:  # это предотвращает ошибку если там чего то нет
            element = soup.find(class_='expansible').find(
                style='color: #625e56;').next_element.next_element.text
            if element is not None:
                expansible.append(element)
            element = soup.find(class_='expansible').find(
                style='color: #625e56;').next_element.next_element.next_element.next_element.text
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
                runes.append(itm1 + ', Тип: ' + itm2)

    def put_data_in_database(self):
        connection = None
        try:
            # подключаемся к базе
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name

            )
            connection.autocommit = True

            # cursor нужен чтобы взаимодействовать с БД
            # сейчас создаем нашу БД
            with connection.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS data (
                        price int NOT NULL,
                        styles text NOT NULL,
                        runes text);"""
                )


        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

a = Parser()
a.put_data_in_database()
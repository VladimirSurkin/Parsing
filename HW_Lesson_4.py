import requests
from lxml import html
from pymongo.errors import DuplicateKeyError
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['dbNews']  # database
vacancy_db = db.vacancy

# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, dzen-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.


header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15'}
response = requests.get('https://lenta.ru', headers=header)

dom = html.fromstring(response.text)

news_lenta = []

items = dom.xpath("//a[contains(@class,'card-mini _topnews')]")
for item in items:
    base_url = 'https://lenta.ru'
    new = {}
    name = item.xpath(".//span[@class='card-mini__title']/text()")
    url = item.xpath(".//@href")
    new_time = item.xpath(".//time[@class='card-mini__date']/text()")

    new['_id'] = str(base_url) + url[0]
    new['name'] = name[0]
    new['new_time'] = new_time
    new['url'] = str(base_url) + url[0]
    news_lenta.append(new)

# 2. Сложить собранные новости в БД Минимум один сайт, максимум - все три

    try:
        vacancy_db.insert_one(new)
    except DuplicateKeyError:
        pprint(f'Новость - {name[0]} уже есть в базе')

pprint(news_lenta)

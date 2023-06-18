# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        client.drop_database('vacancies')
        self.mongo_base = client.vacancies


    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary'] = self.process_salary_hh(item['salary'])
        # collections = self.mongo_base[spider.name]

        collection = self.mongo_base[spider.name]

        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            pprint(f'Вакансия c _ID = {item["_id"]} уже есть в базе - {item["name"]}')

        # collections.insert_one(item)

        return item

    def process_salary_hh(self, salary):
        print (salary)
        type(salary)

        if salary == []:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = [item.replace("\xa0", "") for item in salary]
            salary = [item.replace(" ", "") for item in salary]
            if salary[0] == 'до':
                salary_min = None
                # salary_max = salary[2]
                salary_max = int(salary[1])
                salary_currency = salary[3]
            elif salary[0] == 'от' and salary[2] == 'до':
                salary_min = int(salary[1])
                salary_max = int(salary[3])
                salary_currency = salary[5]
            else:
                salary_min = int(salary[1])
                salary_max = None
                salary_currency = salary[3]

        # salary={}

        # salary.append({'salary_min': salary_min})
        # salary.append({'salary_max': salary_max})
        # salary.append({'salary_currency': salary_currency})
        salary = {'salary_min': salary_min, 'salary_max': salary_max, 'salary_currency': salary_currency}

        return salary
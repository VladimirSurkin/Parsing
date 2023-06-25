# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint
# import os
# from urllib.parse import urlparse

class CastoramaPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.Castorama

    def process_item(self, item, spider):

        collection = self.mongobase[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            pprint(f"Товар c _ID = {item.get('_id')} уже есть в базе")
            pprint(collection)
        return item


class CastoramaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img in item['photos']:
            try:
                yield scrapy.Request(img)
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    # Изображения сохраняются в отдельные папки по названию собираемому товару
    def file_path(self, request, response=None, info=None, *, item=None):
        folder = f"{item.get('link').split('/')[3]}/"
        return folder + super().file_path(request, response=response, info=info, item=item)

    # папка общая, файлы группируютмя по ID изображения

    # def file_path(self, request, response=None, info=None, *, item=None):
    #     folder = f"{item.get('link').split('/')[3]}/"
    #     return {folder} + os.path.basename(urlparse(request.url).path)
    #     # return 'files/' + os.path.basename(urlparse(request.url).path)


    # переименование файла по ID и название. Не рабочий вариант много изображений теряются.

    # def file_path(self, request, response=None, info=None, *, item=None):
    #     # image_filename = f"{item.get('_id')}/"
    #     img_folder = item.get('link').split('/')[3]
    #     # image_filename = f"{img_folder}_{item.get('photos')[-1].split('/')[-1].split('.')[0]}.jpg"
    #     image_filename = f"{img_folder}_{item.get('photos')[-1].split('https://www.castorama.ru/upload/iblock/')[-1].replace('/', '_')}"
    #     # item.get('photos')[-1].split('https://www.castorama.ru/upload/iblock/')[-1].replace('/', '_')
    #     # return fold + super().file_path(request, response=response, info=info, item=item)
    #     return image_filename




# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

#name
def clean_name(value):
    try:
        new_value = value.replace('\n', '').replace('  ', '')
    except Exception as e:
        print(f' Ошибка {e}')
        return new_value
    return new_value

def get_photos_list(photos_list):
    photos_to_download = []
    for photo in photos_list:
        prefix = "/"
        if photo.startswith(prefix):
            photo = 'https://www.castorama.ru' + photo
            photos_to_download.append(photo)
        # photos_to_download.append(photo)
    return photos_to_download

class CastoramaItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clean_name))
    price = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=Compose(get_photos_list))
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    salary = scrapy.Field()
    company_job = scrapy.Field()
    # address = scrapy.Field()

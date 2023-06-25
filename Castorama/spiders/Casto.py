import scrapy
from Castorama.items import CastoramaItem
from scrapy.loader import ItemLoader

class CastoSpider(scrapy.Spider):
    name = "Casto"
    allowed_domains = ["castorama.ru"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('search')}"]
    # start_urls = ["https://www.castorama.ru/catalogsearch/result/?q=мебель"]
        self.start_urls = [f'https://www.castorama.ru/gardening-and-outdoor/outdoor-furniture/']

    def parse(self, response):

        next_page = response.xpath("//div[@class='pages']//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class='product-card__img-link']")
        for link in links:
            yield response.follow(link, callback=self.obj_parse)

    def obj_parse(self, response):
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('_id', "//div[@class='product-essential__sku']/span/text()")
        loader.add_xpath('name', "//h1[@class='product-essential__name hide-max-small']/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//span[@class='price']/span/span/text()")
        loader.add_xpath('currency', "//span[@class='price']//span[@class='currency']/text()")
        loader.add_xpath('photos', "//div[@class='js-zoom-container']/img[@class='top-slide__img swiper-lazy']/@data-src")
        yield loader.load_item()

        # _id = response.xpath("//div[@class='product-essential__sku']/span/text()")get()

        # name = response.xpath("//h1/text()").get()
        # price = response.xpath("//span[@class='price']/span/span/text()").get()
        # currency = response.xpath("//span[@class='price']//span[@class='currency']/text()").get()
        # link = response.url
        # # photos = response.xpath("//div[@class='js-zoom-container']/img[@role='presentation']/@src").getall()
        # photos = response.xpath("//div[@class='js-zoom-container']/img[@class='top-slide__img swiper-lazy']/@data-src").getall()
        #
        # yield CastoramaItem(name=name, price=price, currency=currency, photos=photos, link=link)
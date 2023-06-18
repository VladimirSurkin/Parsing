import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import re

class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?text=python&area=1"]

    def parse(self, response:HtmlResponse, **kwargs):
        links = response.xpath("//a[@class='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath("//a[@class='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response:HtmlResponse):
        _id = re.findall('\d+', response.url)[0]
        name = response.xpath("//h1/text()").get()
        url = response.url
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        # address = response.xpath('//span[@data-qa="vacancy-view-raw-address"]//text()').getall()
        company_job = response.xpath('//span[@class="vacancy-company-name"]//text()').getall()

        # yield JobparserItem(name=name, url=url, salary=salary, address=address, company_job=company_job, vacancy_id=vacancy_id)
        yield JobparserItem(name=name, url=url, salary=salary, company_job=company_job, _id=_id)



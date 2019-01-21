# -*- coding: utf-8 -*-
import scrapy
from ..items import JdSeleniumItem


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']
    base_url = 'https://search.jd.com/Search?keyword={}&page={}'

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, 100, 2):
                url = self.base_url.format(keyword, page)
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        selector = response.xpath("//*[@id='J_goodsList']/ul//li[@class='gl-item']")
        print('---------------------------------------------------')
        print(len(selector))
        print('---------------------------------------------------')
        for item in selector:
            title = ''.join(item.xpath(".//div[4]/a/em//text()").getall())
            price = ''.join(item.xpath(".//div[3]/strong//text()").getall())
            comments = ''.join(item.xpath(".//div[5]/strong//text()").getall())
            item = JdSeleniumItem(title=title, price=price, comments=comments)
            yield item



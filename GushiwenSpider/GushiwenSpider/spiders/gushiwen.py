# -*- coding: utf-8 -*-
import scrapy
from GushiwenSpider.items import GushiwenspiderItem

class GushiwenSpider(scrapy.Spider):
    name = 'gushiwen'
    allowed_domains = ['www.gushiwen.org']
    start_urls = ['https://www.gushiwen.org/shiwen/']

    def parse(self, response):
        poems = response.xpath('//div[@class="left"]/div[@class="sons"]/div[@class="cont"]')
        for poem in poems:
            item = GushiwenspiderItem()
            item['title'] = poem.xpath('./p[1]/a/b/text()').extract_first()
            au_list = poem.xpath('./p[2]/a/text()').extract()
            if len(au_list) < 2:
                au_list.append('')
            item['industry'], item['author'] = au_list
            item['content'] = ''.join(poem.xpath('./div[2]/text() | ./div[2]/p/text()').extract())
            yield item
        next = response.xpath('//a[@class="amore"]/@href').extract_first()
        url = self.start_urls[0][:-8] + next
        yield scrapy.Request(url, callback=self.parse)
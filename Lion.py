# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class LionSpider(scrapy.Spider):
    name = "Lion"

    start_urls = ['http://www.thelion.com/bin/forum.cgi?sf=OIL']

    def parse(self, response):
        thread=response.xpath('//tr/td[@class="tdwrap"]/a/@href').extract()
        for title in thread:
            absolute_url='http://www.thelion.com'+title
            yield Request(absolute_url,callback=self.parse_title)

        next_page_url = response.xpath('//tr/td/a[text()="< Prev 25"]/@href').extract_first()
        absolute_next_page_url='http://www.thelion.com'+next_page_url
        yield Request(absolute_next_page_url,callback=self.parse)


    def parse_title(self,response):
        author=response.xpath('//tr/td[@style="white-space:nowrap;font-size:9pt"]/a[contains(@href,"/bin/profile.cgi?")]/text()').extract_first()
        date=response.xpath('//tr[@class="z"]/td[@class="r"]/text()').extract_first()
        content=response.xpath('//span[@class="a10"]/text()').extract()
        yield {"author": author,
               "date":date,
               "content":content}


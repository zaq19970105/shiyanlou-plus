#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from shiyanlougithub.items import RepositoryItem

class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        for repy in response.css('li.col-12'):
            item = RepositoryItem()
            item['name'] = repy.css('div h3 a::text').re_first('\s*(.+)')
            item['update_time'] = repy.css('div relative-time::attr(datetime)').extract_first()
            url = response.urljoin(repy.css('div h3 a::attr(href)').extract_first())
            request = scrapy.Request(url, callback=self.parse_CBR)
            request.meta['item'] = item
            
            print('turn to another page!!!!!!!!!')
            yield request

        print('Follow!!!!!!!!!!')
        if response.css('div.pagination a::text').extract()[-1] == 'Next':
            url = response.css('div.pagination a::attr(href)').extract()[-1]
            yield scrapy.Request(url=url, callback=self.parse)


    def parse_CBR(self, response):
        item = response.meta['item']

        numbers = response.css("span.num.text-emphasized::text").extract()
        print(numbers)

        item['commits'] = int(numbers[0].replace(',', '').strip())
        item['branches'] = int(numbers[1].replace(',', '').strip())
        item['releases'] = int(numbers[2].replace(',', '').strip())

        yield item

















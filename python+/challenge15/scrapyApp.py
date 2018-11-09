# -*- coding:utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
import requests



class ShiyanlouCoursesSpider(scrapy.Spider):
    name = 'shiyanlou-repositories'

    def start_requests(self):
        url_tmpl = 'https://github.com/shiyanlou?tab=repositories'
        urls = []

        while url_tmpl:
            urls.append(url_tmpl)

            print(url_tmpl)

            r = requests.get(url_tmpl)
            resp = HtmlResponse(url=r.url, body=r.text.encode('utf-8'))

            _ = resp.css('div.pagination a::attr(href)').extract()
            if len(_) == 2: url_tmpl = _[-1]
            else:
                if resp.css('div.pagination a::text').extract_first() == 'Next':
                    url_tmpl = _[0]
                else: url_tmpl = None

        print("Urls had got!")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for repy in response.css('li.col-12.d-block.width-full.py-4.border-bottom.public.source'):
            yield{
                'name': repy.css('div h3 a::text').re_first('\s*(.+)'),
                'update_time': repy.css('div relative-time::attr(datetime)').extract_first()
                }



















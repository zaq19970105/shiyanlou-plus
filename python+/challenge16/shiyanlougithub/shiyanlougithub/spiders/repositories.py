#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from shiyanlougithub.items import RepositoryItem

class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    allowed_domains = ['github.com']

    def start_requests(self):
        urls = ['https://github.com/shiyanlou?tab=repositories', 'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoxOTo1NyswODowMM4FkpYw&tab=repositories', 'https://github.com/shiyanlou?before=Y3Vyc29yOnYyOpK5MjAxNC0xMS0xOVQxMDoxMDoyMyswODowMM4BmcsV&tab=repositories', 'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yMFQxMzowMzo1MiswODowMM4BjkvL&tab=repositories']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for repy in response.css('li.col-12.d-block.width-full.py-4.border-bottom.public.source'):
            item = RepositoryItem({
                'name': repy.css('div h3 a::text').re_first('\s*(.+)'),
                'update_time': repy.css('div relative-time::attr(datetime)').extract_first()
                })
            yield item



















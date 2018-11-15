# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from flask_doc.items import PageItem
import re

class FlaskSpider(scrapy.spiders.CrawlSpider):
    name = 'flask'
    allowed_domains = ['flask.pocoo.org']
    start_urls = ["http://flask.pocoo.org/docs/1.0/"]

    rules = (
            Rule(LinkExtractor(allow="http://flask.pocoo.org/docs/1.0/.*"), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        item = PageItem()
        item['url'] = response.url
        #item['text'] = [x for x in response.css('::text').re('^\s*(.*?)\s*$') if x != '']
        item['text'] = response.css('::text').extract()
        item['text'] = ' '.join(item['text'])
        item['text'] = re.sub('\s+', ' ', item['text'])
        yield item


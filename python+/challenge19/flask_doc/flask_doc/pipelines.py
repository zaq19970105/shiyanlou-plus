# -*- coding: utf-8 -*-

import re
import redis
import json


class FlaskDocPipeline(object):
    def process_item(self, item, spider):
        self.redis.lpush('flask_doc:items', json.dumps(dict(item)))
        return item

    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

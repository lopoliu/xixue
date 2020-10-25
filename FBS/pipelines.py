# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis


class MasterPipelines(object):
    redis_server = None
    def open_spider(self, spider):
        self.redis_server = redis.StrictRedis(host='192.168.0.111', port=6379, db=0)

    def process_item(self, item, spider):
        self.redis_server.sadd('fbs:urls', item['url'])

    def close_spider(self, spider):
        self.redis_server.close()

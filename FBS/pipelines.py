# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import pymongo


class MasterPipelines(object):
    redis_server = None

    def open_spider(self, spider):
        self.redis_server = redis.StrictRedis(host='192.168.0.111', port=6379, db=0)

    def process_item(self, item, spider):
        self.redis_server.sadd('fbs:urls', item['url'])

    def close_spider(self, spider):
        self.redis_server.close()


class SlavePipelines(object):
    conn = None
    tab = None

    def open_spider(self, spider):
        self.conn = pymongo.MongoClient('mongodb://192.168.0.111:27017')
        db = self.conn['yb']
        self.tab = db['info']

    def process_item(self, item, spider):
        info = dict(
            title=item['title'],
            number=item['number']
        )
        self.tab.insert_one(info)

    def close_spider(self, spider):
        self.conn.close()

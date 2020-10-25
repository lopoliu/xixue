# -*- coding: utf-8 -*-
import scrapy
from FBS.items import FbsItem
from scrapy_redis import spiders
import copy


class YbSpiderSpider(spiders.RedisSpider):
    name = 'yb_spider'
    redis_key = 'yb'

    # allowed_domains = ['xxx.com']
    # start_urls = ['http://xxx.com/']

    # def start_requests(self):
    #     yield scrapy.Request('http://www.yiban.cn/square/index')

    def parse(self, response):
        urls = response.xpath('//strong/a/@href').extract()
        addr = response.xpath("//span[@class='location']/text()").extract()
        for i, url in enumerate(urls):
            item = FbsItem()
            item['addr'] = addr[i]
            yield scrapy.Request(
                'http://www.yiban.cn' + url,
                callback=self.parse_detail,
                meta={'item': copy.deepcopy(item)}
            )
        next_page = response.xpath('//div[@class="pager"]/a[@class="next"]/@href').extract_first()
        if next_page:
            yield scrapy.Request('http://www.yiban.cn' + next_page, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta.get('item')
        title = response.xpath('//h2/text()').extract_first()
        number = response.xpath('//div[@class="member-bd"]/div/span/text()').extract_first()
        item['title'] = title
        item['number'] = number
        yield item

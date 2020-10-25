from scrapy_redis.spiders import RedisSpider
from FBS.items import SlaveItem


class SlaveSpider(RedisSpider):
    name = 'slave'
    redis_key = 'fbs:urls'

    custom_settings = {
        'ITEM_PIPELINES': {
            'FBS.pipelines.SlavePipelines': 400
        }
    }

    def parse(self, response):
        item = SlaveItem()
        title = response.xpath('//h2/text()').extract_first()
        number = response.xpath('//span[@class="member-number"]/text()').extract_first()
        item['title'] = title
        item['number'] = number
        yield item

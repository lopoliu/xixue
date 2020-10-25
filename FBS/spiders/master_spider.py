import scrapy
from FBS.items import MasterItem


class MasterSpider(scrapy.Spider):
    name = 'master'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': None,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
        },
        "ITEM_PIPELINES": {
            'FBS.pipelines.MasterPipelines': 400
        },
        'CONCURRENT_REQUESTS': 1
    }

    def start_requests(self):
        yield scrapy.Request('http://www.yiban.cn/square/index')

    def parse(self, response):
        urls = response.xpath('//strong/a/@href').extract()
        # addr = response.xpath("//span[@class='location']/text()").extract()
        for i, url in enumerate(urls):
            item = MasterItem()
            item['url'] = "http://www.yiban.cn" + url
            # item['url'] = "http://www.yiban.cn" + url + '|' + addr[i]
            yield item
        next_page = response.xpath('//div[@class="pager"]/a[@class="next"]/@href').extract_first()
        if next_page:
            yield scrapy.Request('http://www.yiban.cn' + next_page, callback=self.parse)

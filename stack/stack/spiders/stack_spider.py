"""_summary_

Yields:
    _type_: _description_
"""
from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem
class StackSpider(Spider):
    """_summary_

    Args:
        Spider (_type_): _description_

    Yields:
        _type_: _description_
    """
    name = 'stack'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['http://stackoverflow.com/questions?pagesize=50&sort=newest',]
    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="s-post-summary--content"]/h3')
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath('a/text()').extract()[0]
            item['url'] = question.xpath('a/@href').extract()[0]

            yield item

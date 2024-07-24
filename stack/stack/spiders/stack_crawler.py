"""_summary_

Yields:
    _type_: _description_
"""
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from stack.items import StackItem


class StackSpider(CrawlSpider):
    """_summary_

    Args:
        CrawlSpider (_type_): _description_

    Yields:
        _type_: _description_
    """
    name = "stack_crawler"
    allowed_domains = ["stackoverflow.com"]
    start_urls = ['http://stackoverflow.com/questions?pagesize=50&sort=newest',]
    rules = [
        Rule(
            LinkExtractor(allow=r'questions\?tab=newest&page=\b[0-9]\b'),
            callback = 'parse',
            follow = True
        )
    ]
    def parse (self, response):
        questions = Selector(response).xpath('//div[@class="s-post-summary--content"]/h3')
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath('a/text()').extract()[0]
            item['url'] = question.xpath('a/@href').extract()[0]
            yield item

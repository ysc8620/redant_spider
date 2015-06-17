# -*- coding: utf-8 -*-
import scrapy,os
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, HtmlResponse
from kan360.common.items import *
from kan360.common.parser import *


class DmozSpider(CrawlSpider):
    name = "zy"
    allowed_domains = ["360kan.com"]
    start_urls = (
        'http://www.360kan.com/',
        'http://www.360kan.com/zongyi/index.html',
        'http://www.360kan.com/zongyi/list.php'
    )

    rules = (

        Rule(LinkExtractor(  allow=r'http://www.360kan.com/?$')),
        Rule(LinkExtractor(allow=r'/zongyi/(\w+).html$')),
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=r'/zongyi/list.php((\?|&)(cat=(all|\d+)|pageno=\d+|area=(\d+|all)|year=|act=|rank=(rankhot|pub))){0,6}$')),
        Rule(LinkExtractor(allow=r'/zongyi/list.php((\?|&)(cat=all|year=|pageno=\d+|area=all|act=[%\w]+)){0,4}$')),
        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=r'/va/(\w+).html$'), callback='parse_item'),
    )

    def __init__(self, *a, **kw):
        infile = os.getcwd()+r'/kan360/websites/360kan_dm.xml'
        self.xml = Selector(text=file(infile,"a+").read(), type='xml')
        self.xpath_object = base_parser()

        super(CrawlSpider, self).__init__(*a, **kw)
        self._compile_rules()

    def parse_item(self, response):
        item = self.xpath_object.run(spider=self, response=response, xml=self.xml)
        return item

if __name__ =='__main__':
    print type([])

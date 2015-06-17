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
    name = "mv"
    allowed_domains = ["360kan.com"]
    start_urls = (
        'http://www.360kan.com/',
        'http://www.360kan.com/dianying/index.html',
        'http://www.360kan.com/vip/index.html',
        'http://www.360kan.com/weidianying/index.html',
        'http://www.360kan.com/top/',
        'http://www.360kan.com/dianying/list.php'
       # 'http://www.360kan.com/m/gKbkYUT7Q0f0UB.html'
    )

    rules = (
        Rule(LinkExtractor(allow=r'/top/detail/((\?|&)(postype=\d+|toptype=\d+|topname=\d+)){0,3}$$')),
        Rule(LinkExtractor(allow=r'/topic/\w+.html$')),
        Rule(LinkExtractor(allow=r'/gene/list.php((\?|&)(kw=[%\w]+|pageno=\d+){0,2}$')),
        Rule(LinkExtractor(allow=r'/gene/mlist.php((\?|&)(kw=[%\w]+|pageno=\d+){0,2}$')),

        Rule(LinkExtractor(allow=r'/dianying/(\w+).html$')),
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=r'/dianying/list.php((\?|&)(cat=(all|\d+)|year=(other|all|\d+)|pageno=\d+|area=(\d+|all)|act=all|rank=(createtime|rankpoint))){0,6}$')),
        Rule(LinkExtractor(allow=r'/dianying/list.php((\?|&)(cat=all|year=all|pageno=\d+|area=all|act=[%\w]+)){0,6}$')),

        Rule(LinkExtractor(allow=r'/dianying/top/.+')),
        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=r'/m/(\w+).html$'), callback='parse_item'),
    )

    def __init__(self, *a, **kw):
        infile = os.getcwd()+r'/kan360/websites/360kan_mv.xml'
        self.xml = Selector(text=file(infile,"a+").read(), type='xml')
        self.xpath_object = base_parser()

        super(CrawlSpider, self).__init__(*a, **kw)
        self._compile_rules()

    def parse_item(self, response):
        item = self.xpath_object.run(spider=self, response=response, xml=self.xml)
        return item

if __name__ =='__main__':
    print type([])

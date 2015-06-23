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
    name = "test"
    allowed_domains = ["360kan.com"]
    start_urls = (
        'http://www.360kan.com/va/YsQkbaNv7JM6Dj.html',
    )

    rules = (
        # Rule(LinkExtractor(  allow=r'http://www.360kan.com/$')),
        # Rule(LinkExtractor(allow=r'/dianying/(\w+).html$')),
        # # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        # Rule(LinkExtractor(allow=r'/dianying/list.php\??(&?(cat=\w+|year=\w+|pageno=\d+|area=\w+|act=all)?){0,6}$')),
        # Rule(LinkExtractor(allow=r'/dianying/top/.+')),
        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=r'/va/YsQkbaNv7JM6Dj.html$'), callback='parse_item'),
    )

    def parse_item(self, response):
        # xpath = base_parser()
        # item = xpath.run(spider=self, response=response, xml=self.xml)
        hsx = Selector(response)
        title = hsx.xpath("//span[@id='film_name']/text()").extract()
        print title[0]
        juji = hsx.xpath("//div[@id='listing']//ul[@id='supplies']/li/@site").extract()
        for ji in juji:
            print ji
        list = hsx.xpath("//div[@id='listing']//div[contains(@class,'listing-bd')]//dl").extract()
        for i in list:
            #print i
            dl = Selector(text=i)
            print dl.xpath('//dt/a/@title').extract()[0]
            print dl.xpath('//dt/a/@href').extract()[0]
            print dl.xpath('//dd/a/img/@src').extract()[0]
            print '=================='


        print response.url

        #print item
        return []

if __name__ =='__main__':
    print type([])

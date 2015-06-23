# -*- coding: utf-8 -*-
import scrapy,os
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request, HtmlResponse
from kan360.common.items import *
from kan360.common.base import *
from kan360.common.parser import *


class DmozSpider(CrawlSpider):
    name = "dmoz"
    allowed_domains = []
    start_urls = []
    rules = ()
    start_time = None
    xml = None

    def __init__(self,name=None,r=None, *a, **kw):
        self.start_time = int(time.time())
        if name == None:
            logs(time.strftime("------%Y-%m-%d %H:%M:%S ") +' Spider Name No Exits.')
            exit(0)

        infile = os.getcwd()+r'/kan360/websites/'+name+'.xml'
        if os.path.exists(infile):
            logs('Spider '+ name + ' Start Read.')
            self.xml = Selector(text=file(infile,"a+").read(), type='xml')
        else:
            logs( 'Spider ' + name +' No Exits.')
            exit(0)

        self.name = self.name +':'+ name
        self.spider_name = name

        # 是否启用爬虫
        enable = self.xml.xpath("//site/@enable").extract()[0].strip()
        if enable != '1':
            if r == None:
                logs(time.strftime("------%Y-%m-%d %H:%M:%S ") +' ' + name +' No Enable.')
                exit(0)
        # 设置匹配模式
        xpath = self.xml.xpath("//site/@xpath").extract()
        if xpath:
            self.xpath_model = xpath[0].strip()

        try:
            self.xpath_object = eval(self.xpath_model+'()')
        except:
            logs(time.strftime("------%Y-%m-%d %H:%M:%S ") +' xpath model not found.')
            exit(0)

        # 设置运行域名
        allowe_url = self.xml.xpath("//site/allowedDomains/url")
        if allowe_url:
            for url in allowe_url:
                #start_url_xpath = Selector(text=url, type='xml')
                link = url.xpath('@url').extract()
                if link:
                    page_url =link[0].strip()
                    self.allowed_domains.append(page_url)

        # 设置起始URL
        start_url = self.xml.xpath("//site/startUrls/url")
        if start_url:
            for url in start_url:
                link = url.xpath('@url').extract()
                if link:
                    page_url = link[0].strip()
                    self.start_urls.append(page_url)

        # 设置链接规则
        url_rule = self.xml.xpath("//site/queueRules/rule")
        rules = []
        for rule in url_rule:
            str_allow = rule.xpath("@rule").extract()
            str_allow = '' if len(str_allow)<1 else str_allow[0].strip()
            str_deny = rule.xpath("@deny").extract()
            str_deny = '' if len(str_deny)<1 else str_deny[0].strip()
            str_callback = rule.xpath("@callback").extract()
            str_callback = '' if len(str_callback)<1 else str_callback[0].strip()

            if str_callback != '':
                if str_deny != '':
                    ru = Rule(LinkExtractor(allow=r""+str_allow, deny=r""+str_deny),callback=str_callback)
                else:
                    ru = Rule(LinkExtractor(allow=r""+str_allow), callback=str_callback)
            else:
                if str_deny != '':
                    ru = Rule(LinkExtractor(allow=r""+str_allow ,deny=r""+str_deny))
                else:
                    ru = Rule(LinkExtractor(allow=r""+str_allow))
            rules.append(ru)

        self.rules = tuple(rules)

        super(CrawlSpider, self).__init__(*a, **kw)
        self._compile_rules()


    def parse_item(self, response):
        item = self.xpath_object.run(spider=self, response=response, xml=self.xml)
        return item


if __name__ =='__main__':
    print type([])

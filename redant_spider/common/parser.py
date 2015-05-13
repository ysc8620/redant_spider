#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from redant_spider.common.items import *
from redant_spider.common.db import *
from redant_spider.common.base import *
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
import urlparse
import time
import re
import json

# 特殊扩展类处理特例
class parser_spread():
    parser = None

    def __init__(self, parser=None):
        self.parser = parser

    def omigo_json_img(self, json_html):
        js_data = json.loads(json_html)
        ret = []
        for i in js_data:
            ret.append( self.parser.get_field_value(i['large'],'img'))
        return ret

    def run(self):
        pass

class parser_attrs:
    attrs = []
    xml = ''

    parser = None
    def __init__(self, parser=None):
        self.parser = parser
        self.attrs = []

    def xml(self, xml=''):
        self.xml = xml
        return self
    def rm(self, attr):
        self.attrs.append(attr)
        return self

    def __rm(self):
        attrs = ''
        for attr in self.attrs:
            attrs = attrs + '|' +attr
        attrs = attrs.strip('|')
        if attrs:
            link = re.compile(r"(<\w+.*?)("+attrs+")\s*?=\s*?['|\"].*?['|\"](.*?>)")
            self.xml = re.sub(link,r'\1\3',self.xml)

    def run(self):
        self.__rm()
        return self.xml

class parser_tags:
    allow_tags = []
    del_tags = []
    isEmpty = False
    xml = ''
    parser = None
    def __init__(self, parser=None):
        self.parser = parser

    def xml(self, xml):
        self.xml = xml
        return self

    def rm(self, tag):
        self.del_tags.append(tag)
        return self

    def kp(self, tag):
        self.allow_tags.append(tag)
        return self

    def empty(self):
        self.isEmpty = True
        return  self

    def __rm(self):
        tags = ''
        for tag in self.del_tags:
            tags = tags+'|'+tag
        tags = tags.strip('|')

        if tags:
            link = re.compile(r"</?("+tags+").*?>", re.I)
            self.xml = re.sub( link, '', self.xml)

    def __kp(self):
        tags = ''
        for tag in self.allow_tags:
            tags = tags + '|' + tag + '|/' + tag
        tags = tags.strip('|')

        if tags:
            link = re.compile(r"<[^("+tags+")].*?>",re.I)
            self.xml = re.sub(link,'',self.xml)

    def __empty(self):
        if self.isEmpty:
            link = re.compile(r"\s+")
            self.xml = re.sub(link,' ', self.xml)

    def run(self):
        self.__rm()
        self.__kp()
        self.__empty()
        return self.xml

class parser:
    hs = url = base_url =''

    def get_field_value(self, value, value_type=None):
        if value_type == 'img':
            return self.get_img_url(value)
        return value


    def get_goods_info(self, arg):
        pass

    def get_img_url(self, url):
        return urlparse.urljoin(self.base_url, url)

    def set_defalut(self, spider=None, response=None, text=None):
        if text!=None:
            self.hs = Selector(text=text,type='xml')
            self.url = ''
            self.base_url = ''
        else:
            self.hs = Selector(response)
            self.url = response.url
            self.base_url = get_base_url(response)


        item = BaseItem()

        for name,value in vars(BaseItem).items():
            if name == 'fields':
                for i in value:
                    if i== 'image_urls' or i == 'images':
                        item[i] = []
                    else:
                        item[i] = {}
        return item

    def parser_item(self, html_parser, item,url,xml):
        # is follow
        follows = xml.xpath("//targets//follow/parser")
        if follows:
            for follow in follows:
                xpath = follow.xpath('@xpath').extract()
                if xpath:
                    url_id = html_parser.xpath(xpath[0]).extract()
                    if url_id:
                        id = url_id[0].strip()
                    else:
                        item['goods']['is_exist_item'] = False
                        return item
                    continue

                val = follow.xpath('@val').extract()
                if val:
                    try:
                        url_id = eval(val[0])
                    except Exception,e:
                        pass
                    if url_id:
                        id = url_id[0].strip()
                    else:
                        item['goods']['is_exist_item'] = False
                        return item
                    continue

        # is has
        website_id = xml.xpath("//site/@website_id").extract()
        if website_id:
            website_id = website_id[0].strip()

        exist_name = xml.xpath("//targets//exist/@name").extract()
        exist_value = ''
        row = False
        if exist_name:
            exist_name = exist_name[0].strip()
            exist_list = xml.xpath("//targets//exist/parser")

            for exist in exist_list:
                xpath = exist.xpath('@xpath').extract()
                if xpath:
                    exist_val = html_parser.xpath(xpath[0]).extract()
                    if exist_val:
                        exist_value = exist_val[0]
                    continue
                val = exist.xpath('@val').extract()
                if val:
                    try:
                        exist_value = eval(val[0])
                    except Exception, e:
                        logs(time.strftime("------%Y-%m-%d %H:%M:%S-")  +val[0] +' eval error.')
                        exit(0)
                    continue
            row = DB.init().getOne("SELECT goods_id, name, price, original_price,isshow,cate_id FROM le_goods WHERE website_id=%s AND "+exist_name+"=%s", [website_id,exist_value])
            if row != False:
                item['rowItem'] = row

        fields = xml.xpath("//targets//model//field")
        for field in fields:
            name = field.xpath("@name").extract()
            define = field.xpath("@def").extract()
            isArray = field.xpath("@isArray").extract()
            filed_type = field.xpath("@type").extract()

            if len(filed_type) > 0:
                filed_type = filed_type[0]
            else:
                filed_type = ''

            if len(name) < 1 :
                logs(time.strftime("------%Y-%m-%d %H:%M:%S") + ' Field Name No Define.')
                exit(0)

            _this = ''
            name = name[0].strip()
            if define:
                if item[name]:
                    _this = item[name]
                else:
                    item[name] = define[0].strip()
                    _this = define[0].strip()

            if isArray:
                if len(item[name]) < 1:
                    item[name] = []
                    _this = []
                else:
                    _this = item[name]
            #field_xml = Selector(text=field.extract()[0])
            field_html = field.extract()
            if field_html:
                field_xml = Selector(text=field_html,type='xml')
                parser_list = field_xml.xpath("//parsers/parser")
                #print parser_list
                for parser in parser_list:
                    _Tags = parser_tags(self)
                    _Attrs = parser_attrs(self)
                    _Spread = parser_spread(self)

                    xpath = parser.xpath("@xpath").extract()
                    if len( xpath ) > 0:
                        re= parser.xpath("@re").extract()
                        for xp in xpath:
                            if re:
                                val = html_parser.xpath(xp).re(re[0])
                            else:
                                val = html_parser.xpath(xp).extract()
                            if isArray:
                                for v in val:
                                    _this.append( self.get_field_value(v.strip(), filed_type))
                            else:
                                if len(val) > 0:
                                    _this = self.get_field_value(val[0].strip(), filed_type)

                        continue

                    rep = parser.xpath("@rep").extract()
                    if len( rep ) > 0:
                        try:
                            _this = eval(rep[0])
                        except Exception, e:
                            logs(time.strftime("------%Y-%m-%d %H:%M:%S") + rep[0]+ ' rep eval error.' + e.message)
                item[name] = _this
        if item['url'] == '':
            item['url'] = self.url

        if item['ExpiryTime']:
            item['ExpiryTime'] = int(item['ExpiryTime'])

        if row == False and item['oldImg']:
            item['image_urls'] = item['oldImg']
        return item

    def run(self, spider=None, response=None, xml=None, text=None):
        return self.set_defalut(spider=spider, response=response, text=text)

class base_parser(parser):

    def run(self, spider=None, response=None, xml=None, text=None):

        model_list = xml.xpath("//targets//model")

        for model in model_list:
            model_xpath = model.xpath("@xpath").extract()
            model_is_array = model.xpath("@xpath").extract()
            if model_is_array:
                if model_xpath:
                    parser_htmls = self.hs.xpath(model_xpath[0])
                    if parser_htmls:
                        for parser_html in parser_htmls:
                            item = self.set_defalut(spider=spider, response=response, text=text)
                            #print parser_html
                            yield self.parser_item(html_parser=parser_html,item=item,url=self.url,xml=xml)
            else:
                item = self.set_defalut(spider=spider, response=response, text=text)
                yield self.parser_item(html_parser=self.hs,item=item,url=self.url,xml=xml)

class xml_parser(parser):

    def run(self, spider=None, response=None, xml=None, text=None):
        model_list = xml.xpath("//targets//model")

        for model in model_list:
            model_xpath = model.xpath("@xpath").extract()
            model_is_array = model.xpath("@xpath").extract()

            if model_is_array:
                if model_xpath:
                    item = self.set_defalut(spider=spider, response=response, text=text)

                    parser_htmls = self.hs.xpath(model_xpath[0])
                    if parser_htmls:
                        for parser_html in parser_htmls:
                            item = self.set_defalut(spider=spider, response=response, text=text)
                            yield self.parser_item(html_parser=parser_html,item=item,url=self.url,xml=xml)
            else:

                item = self.set_defalut(spider=spider, response=response, text=text)
                yield self.parser_item(html_parser=self.hs,item=item,url=self.url,xml=xml)



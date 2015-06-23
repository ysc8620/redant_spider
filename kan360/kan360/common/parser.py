#!/usr/bin/python
#coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from kan360.common.items import *
from kan360.common.db import *
from kan360.common.base import *
from kan360.common.expand import *
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
import urlparse,time,re,json

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

    def get_img_url(self, url):
        return urlparse.urljoin(self.base_url, url)

    def set_defalut(self, spider=None, response=None, text=None,xml=None):
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
        sqlfields = xml.xpath('//sqlfields/fields/@name').extract()
        item['rowItem']['sqlfields'] = sqlfields[0]

        sqlfields = xml.xpath('//sqlfields/fields/@update').extract()
        item['rowItem']['updatesqlfields'] = sqlfields[0]

        # is follow
        follows = xml.xpath("//targets//isFollow/parser")
        if follows:
            for follow in follows:
                xpath = follow.xpath('@xpath').extract()
                if xpath:
                    url_id = html_parser.xpath(xpath[0]).extract()
                    if url_id:
                        id = url_id[0].strip()
                    else:
                        item['rowItem']['is_exist_item'] = False
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
                        item['rowItem']['is_exist_item'] = False
                        return item
                    continue

        # is has
        website_id = xml.xpath("//site/@website_id").extract()
        if website_id:
            website_id = website_id[0].strip()

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
                if item['rowItem'].has_key(name):
                    _this = item['rowItem'][name]
                else:
                    item['rowItem'][name] = define[0].strip()
                    _this = define[0].strip()

            if isArray:
                if item['rowItem'].has_key(name) != True:
                    item['rowItem'][name] = []
                    _this = []
                else:
                    if len(item['rowItem'][name])>0:
                        continue
                    else:
                        item['rowItem'][name] = []
                        _this = []
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
                                if len(val)>0:
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
                            print rep[0],_this
                            logs(time.strftime("------%Y-%m-%d %H:%M:%S") + rep[0]+ ' rep eval error.' + e.message)
                item['rowItem'][name] = _this
        if item['rowItem'].has_key('url') == False:
            item['rowItem']['url'] = self.url
        bool = False
        row = False
        # if item['rowItem'].has_key('site_id'):
        #     if item['rowItem']['site_id']:
        #         bool = True
        #         row = DB.init().getOne("SELECT id,site_id FROM js_vods WHERE website_id=%s AND site_id=%s", [website_id,item['rowItem']['site_id']])
        #         if row != False:
        #             item['rowItem']['exits_item'] = row

        if bool == False and row == False:
            if item['rowItem'].has_key('url'):
                if item['rowItem']['url']:
                    #bool = True
                    ## website_id=%s AND
                    row = DB.init().getOne("SELECT id,url FROM js_vods WHERE url=%s", [item['rowItem']['url']])
                    if row != False:
                        item['rowItem']['exits_item'] = row

        if row == False and item['rowItem'].has_key('old_pic'):
            if item['rowItem']['old_pic']:
                if type(item['rowItem']['old_pic']) == list:
                    item['image_urls'] = item['rowItem']['old_pic']
                elif type(item['rowItem']['old_pic']) == str or type(item['rowItem']['old_pic']) == unicode:
                    item['image_urls'] = [item['rowItem']['old_pic']]

        afterParser = xml.xpath("//afterParser/field")

        if afterParser:
            for field in afterParser:
                parser_list = field.xpath("parsers/parser/@rep").extract()
                name = field.xpath('@name').extract()
                try:
                    name = name[0]
                    for parser in parser_list:
                        data = eval(parser)
                        item['rowItem'][name] = data
                except Exception, e:
                    logs(time.strftime("------%Y-%m-%d %H:%M:%S")+' afterParser rep eval error.' + e.message)
                    print e
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
                            item = self.set_defalut(spider=spider, response=response, text=text,xml=xml)
                            yield self.parser_item(html_parser=parser_html,item=item,url=self.url,xml=xml)
            else:
                item = self.set_defalut(spider=spider, response=response, text=text,xml=xml)
                yield self.parser_item(html_parser=self.hs,item=item,url=self.url,xml=xml)

class xml_parser(base_parser):

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
                            item = self.set_defalut(spider=spider, response=response, text=text,xml=xml)
                            yield self.parser_item(html_parser=parser_html,item=item,url=self.url,xml=xml)
            else:
                item = self.set_defalut(spider=spider, response=response, text=text,xml=xml)
                yield self.parser_item(html_parser=self.hs,item=item,url=self.url,xml=xml)


class test_parser(base_parser):

    def run(self, spider=None, response=None, xml=None, text=None):
        model_list = xml.xpath("//targets//model")
        for model in model_list:
            model_xpath = model.xpath("@xpath").extract()
            model_is_array = model.xpath("@xpath").extract()
            if model_is_array:
                if model_xpath:
                    item = self.set_defalut(spider=spider, response=response, text=text,xml=xml)
                    parser_htmls = self.hs.xpath(model_xpath[0])
                    if parser_htmls:
                        for parser_html in parser_htmls:
                            item = self.set_defalut(spider=spider, response=response, text=text,xml=xml)
                            return self.parser_item(html_parser=parser_html,item=item,url=self.url,xml=xml)
            else:
                item = self.set_defalut(spider=spider, response=response, text=text)
                return self.parser_item(html_parser=self.hs,item=item,url=self.url,xml=xml)
__author__ = 'ShengYue'
import sys,os,re
from datetime import *
from common.db import *
from w3lib.encoding import html_to_unicode
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
from common.download import *

#import lxml.html.soupparser as soupparser

class myspider:
    allow_url = []
    def __init__(self):
        self.allow_url = [
             'http://www.360kan.com/m/f6fjYxH1QHH6UR.html',
        ]

    def factory(self,data, parser_cls,url):
        charset = 'charset=%s' % 'utf-8'
        data = html_to_unicode(charset, data)[1]
        body = data.encode('utf8') or '<html/>'


        parser = parser_cls(recover=True, encoding='utf8')
        return etree.fromstring(body, parser=parser, base_url=url)

    def p(self,data,url='',parser=etree.HTMLParser):
        return self.factory(data, parser,url)


    def extract(self):
        try:
            return etree.tostring(self._root,
                                  method=self._tostring_method,
                                  encoding=unicode,
                                  with_tail=False)
        except (AttributeError, TypeError):
            if self._root is True:
                return u'1'
            elif self._root is False:
                return u'0'
            else:
                return unicode(self._root)

    def run(self):
        zy=200
        dy=200
        tv=200
        dm=200
        splider=BrowserBase()
        for i in self.allow_url:
            data = splider.read(i)
            html =  self.p(data,i)
            links = html.xpath("//div[@class='aggregate-rating']//div[contains(@class,'rating-site')]//p[@class='value']/span")
            print etree.tostring(links[0])
if __name__=='__main__':
    d = myspider()
    d.run()

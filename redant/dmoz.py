__author__ = 'ShengYue'
import sys,os,re
from common.db import *
from w3lib.encoding import html_to_unicode
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree
from common.download import *
class myspider:
    allow_url = []
    def __init__(self):
        self.allow_url = [
            'http://www.360kan.com/',
             'http://www.360kan.com/dianying/index.html',
             'http://www.360kan.com/dianshi/index.html',
             'http://www.360kan.com/dongman/index.html',
             'http://www.360kan.com/zongyi/index.html',
        ]

    def factory(self,data, parser_cls,url):
        charset = 'charset=%s' % 'utf-8'
        data = html_to_unicode(charset, data)[1]
        body = data.encode('utf8') or '<html/>'
        parser = parser_cls(recover=True, encoding='utf8')
        return etree.fromstring(body, parser=parser, base_url=url)

    def p(self,data,url='',parser=etree.HTMLParser):
        return self.factory(data, parser,url)

    def run(self):
        zy=200
        dy=200
        tv=200
        dm=200
        splider=BrowserBase()
        for i in self.allow_url:
            data = splider.read(i)
            html =  self.p(data.strip(),i)
            links = html.xpath("//a/@href")
            for i in links:
                m = re.search(r'(http://www.360kan.com)?/(ct|va|m|tv)/(\w+).html', i)
                if m :
                    if i[0] == '/':
                        i = 'http://www.360kan.com'+i
                    #print i
                    row = DB.init().getOne("SELECT id,url,pic FROM js_vods WHERE url=%s", [i])
                    print row
                    if "/va/" in i:
                        zy = zy - 0.001
                        print 'zy:', zy, ' ', i
                    if "/m/" in i:
                        dy = dy - 0.001
                        print 'm: ', dy, ' ', i
                    if "/tv/" in i:
                        tv = tv - 0.001
                        print 'tv: ', tv, ' ', i
                    if "/ct/" in i:
                        dm = dm - 0.001
                        print 'dm: ', dm, ' ', i

if __name__=='__main__':
    d = myspider()
    d.run()

#!/usr/bin/python
#coding=utf-8
import sys,os,time,json,re,urllib2,json
from base import *
from scrapy.selector import Selector


reload(sys)
sys.setdefaultencoding('utf8')

def parse_mv_jump_url(data):
    #print data
    #exit(0)
    ret = ''
    if data:
        for i in data:

            hts = Selector(text=i)
            text = hts.xpath("//em/text()").extract()
            href = hts.xpath("//a/@href").extract()
            if len(text) > 0:
                if len(text[0].strip()) > 0:
                    name = text[0].strip()
                else:
                    continue
            else:
                text = hts.xpath("//a//span[@class='info left']/text()").extract()
                if len(text) > 0:
                    if len(text[0].strip()) > 0:
                        name = text[0].strip()
                    else:
                        continue
                else:
                    text = hts.xpath("//a/@sitename").extract()
                    if len(text) > 0:
                        if len(text[0].strip()) > 0:
                            name = text[0].strip()
                        else:
                            continue
                    else:
                        continue
            if len(href) > 0:
                if len(href[0].strip())>0:
                    url = href[0].strip()
                else:
                    continue
            else:
                continue

            ret += name+'$'+url+"\n"
            ret = ret.strip()+"$$$"
    ret = ret.strip('$$$')
    #print ret
    return ret

def parse_dm_jump_url(data):
    ret = old_sitename = ''
    if data:
        for i in data:
            hts = Selector(text=i)
            text = hts.xpath("//a/text()").extract()
            href = hts.xpath("//a/@href").extract()
            sitename = hts.xpath("//a/@sitename").extract()
            if old_sitename:
                if old_sitename != sitename:
                    ret = ret.strip()+"$$$"
            old_sitename = sitename
            if len(text) > 0:
                if len(text[0].strip()) > 0:
                    name = text[0].strip()
                else:
                    continue
            else:
                continue
            if len(href) > 0:
                if len(href[0].strip())>0:
                    url = href[0].strip()
                else:
                    continue
            else:
                continue

            ret += name+'$'+url+"\n"

    ret = ret.strip('$$$')
    return ret

def parse_jump_url(data):
    ret = ''
    if data:
        for i in data:
            hts = Selector(text=i)
            value = hts.xpath("//a[@playtype='tv']")
            for a in value:
                name = url = ''
                text = a.xpath("text()").extract()
                href = a.xpath("@href").extract()
                if len(text) > 0:
                    if len(text[0].strip()) > 0:
                        name = text[0].strip()
                    else:
                        continue
                else:
                    continue
                if len(href) > 0:
                    if len(href[0].strip())>0:
                        url = href[0].strip()
                    else:
                        continue
                else:
                    continue

                ret += name+'$'+url+"\n"
            ret = ret.strip()+"$$$"
    ret = ret.strip('$$$')
    #print ret
    return ret

def zy(data,ret):
    #print data, ret
    hs = Selector(text=data['data'])
    dl = hs.xpath("//dl").extract()
    for i in dl:
        dls =   Selector(text=i)
        href = dls.xpath('//a/@href').extract()
        if len(href)>0:
            str_href = href[0].strip()
        else:
            str_href = ''
        text = dls.xpath('//div[@class="intro-txt"]/text()').extract()
        if len(text)>0:
            str_text = text[0].strip()
        else:
            str_text = ''
        num = dls.xpath('//a/@playno').extract()
        if len(num) > 0:
            str_num = num[0].strip()
        else:
            str_num = ''

        ret['jump_url']  += str_num+'$'+str_text+'$'+str_href+"\n"

        img = dls.xpath('//img/@src').extract()
        if len(img)>0:
            str_img = img[0].strip()
        else:
            str_img = ''
        title = dls.xpath('//a/@title').extract()
        if len(title)>0:
            str_title = title[0].strip()
        else:
            str_title = ''
        ret['jump_info']  += str_num +'$'+ str_title+'$'+str_img+"\n"
    return ret

def parse_zy(pay_type,url):
    rs = re.search(r'.*?/va/(\w+).html',url)
    if rs:
        id = rs.group(1)
    else:
        id = ''
        return {'jump_url':'', 'jump_info':''}
    #id = 'ZsMmcKZv7ZMBDD'
    #http://www.360kan.com/va/YcQla6dv7JM8Dz.html
    # http://www.360kan.com/cover/zongyilist?id=asYra6Nw7Jc7Ez&do=showpage&site=sohu&pageno=2
    ret = {'jump_url':'', 'jump_info':''}

    pay_list = pay_type.split('$$$')
    #print pay_list
    if pay_list:
        # 获取其他type综艺信息
        for site in pay_list:
            #va/YcUmb3Nu8Jg2FT.html
            #http://www.360kan.com/cover/zongyilist?id=ZMEkbaRv82I5ET&do=showpage&site=cntv&pageno=3
            url = "http://www.360kan.com/cover/zongyilist?id="+id+"&do=switchsite&site="+site.strip()
            print url
            f = urllib2.urlopen(url)
            data = f.read()
            #print data
            djson = json.loads(data)
            pages = 1
            #print djson
            if djson['data']:
                #print djson['data']
                hs = Selector(text=djson['data'])
                pagesize = hs.xpath("//a[@class='lastPage']/@pagenum").extract()
                if pagesize:
                    pages = int(pagesize[0].strip())

                ret = zy(djson, ret)

                if pages > 1:
                    max = pages+1
                    for page in range(2,max):
                        url = "http://www.360kan.com/cover/zongyilist?id="+id+"&do=showpage&site="+site.strip()+"&pageno="+str(page)
                        print url
                        f = urllib2.urlopen(url)
                        data = f.read()
                        djson = json.loads(data)
                        if djson['data']:

                            ret = zy(djson, ret)
                ret['jump_url'] = ret['jump_url'].strip()+"$$$"
                ret['jump_info'] = ret['jump_info'].strip()+"$$$"

    ret['jump_url'] = ret['jump_url'].strip('$$$')
    ret['jump_info'] = ret['jump_info'].strip('$$$')
    #print ret
    return ret

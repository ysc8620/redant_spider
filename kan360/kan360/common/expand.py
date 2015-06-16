#!/usr/bin/python
#coding=utf-8
import sys,os,time,json
from base import *
from scrapy.selector import Selector


reload(sys)
sys.setdefaultencoding('utf8')

def parse_mv_jump_url(data):
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
                text = hts.xpath("//a/text()").extract()
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
    ret = ''
    if data:
        for i in data:
            hts = Selector(text=i)
            text = hts.xpath("//a/text()").extract()
            href = hts.xpath("//a/@href").extract()
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
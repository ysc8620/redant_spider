#!/usr/bin/python
#coding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding('utf8')
import redis


class redisDB:
    conn = None
    r = None
    def connect(self):
        if self.conn:
            pass
        else:
            try:
                self.conn = redis.StrictRedis(host='127.0.0.1', port=6379)
            except:
                print 'Redis Connect error.'

    u'清空指定爬虫数据'
    def flushSpider(self, spider):
        print u'开始清空爬虫对应redis信息'
        self.connect()
        self.conn.delete('dmoz:'+spider+':requests')
        self.conn.delete('dmoz:'+spider+':dupefilter')
        self.conn.delete('dmoz:'+spider+':items')
        print u'redis数据清空完毕'

    u'清空所有数据'
    def flushAll(self):
        print self.conn.flushall()

    def close(self):
        pass


# s = redisDB()
# s.flushSpider('imobshop')
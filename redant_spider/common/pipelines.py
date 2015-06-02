#!/usr/bin/python
#coding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding('utf8')

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
from redant_spider.common.db import DB
from redant_spider.common.base import *
from redant_spider.common.items import *
from redant_spider.common.expand import *

#
'''
商品结构
_id,  unique_id(唯一编号 md5(website + website_goods_id )), title, price, original_price, img,
img_list( 数组 多图片), brand, category, category_list(数组 分类组合)
description, from_url, from_website(来自网站), status(1默认显示， 2 隐藏，), add_time, update_time
'''
class BasePipeline(object):
    conn = None

    def add_cate_goods_index(self, cate_id, goods_id):
        DB.init().insertOne("INSERT INTO le_cate_goods_index SET cate_id=%s, goods_id=%s,weight=0",[cate_id, goods_id])
        DB.init().end()
    '''
   #
    '''
    def process_item(self, item, spider):

        if type(item) != BaseItem:
            return item

        if item['rowItem'].has_key('is_exist_item'):
            if item['rowItem']['is_exist_item'] == False:
                return item

        for i in item:
            if type(item[i]) == unicode or type(item[i]) == str:
                 item[i] = item[i].encode('utf-8')
        # if item['rowItem']:
        #     if item['goods']['price'] != item['price'] or item['goods']['original_price'] != item['originalPrice'] or item['goods']['name'] != item['name']:
        #         DB.init().update("UPDATE le_goods SET isshow=1,name=%s,price=%s,original_price=%s, uptime=%s,expiry_time=%s,site_id=%s,cate_id=%s WHERE goods_id=%s",[item['name'],item['price'],item['originalPrice'],int(time.time()),item['ExpiryTime'], item['site_id'],goods_cate_id,item['goods']['goods_id']])
        #     else:
        #         DB.init().update("UPDATE le_goods SET isshow=1,uptime=%s,expiry_time=%s,site_id=%s WHERE goods_id=%s",[int(time.time()),item['ExpiryTime'], item['site_id'],goods_cate_id,item['goods']['goods_id']])
        #     DB.init().end()
        # else:
        fields_id = item['rowItem']['sqlfields'].split(',')
        sql = "INSERT INTO js_vods SET "
        data = []
        for i in fields_id:
            sql += "i=%s ,";
            data.append(item['rowItem'][i])
        sql = sql.strip(',')
        DB.init().insertOne('"'+sql+'"',data)
        #DB.init().end()
        return item


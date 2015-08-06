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
from kan360.common.db import DB
from kan360.common.base import *
from kan360.common.items import *
from kan360.common.expand import *

#
'''
商品结构
_id,  unique_id(唯一编号 md5(website + website_goods_id )), title, price, original_price, img,
img_list( 数组 多图片), brand, category, category_list(数组 分类组合)
description, from_url, from_website(来自网站), status(1默认显示， 2 隐藏，), add_time, update_time
'''
class BasePipeline(object):
    conn = None
    '''
    '''
    def process_item(self, item, spider):

        if type(item) != BaseItem:
            return item

        if item['rowItem'].has_key('is_exist_item'):
            if item['rowItem']['is_exist_item'] == False:
                return item

        for i in item['rowItem']:
            if type(item['rowItem'][i]) == unicode or type(item['rowItem'][i]) == str:
                 item['rowItem'][i] = item['rowItem'][i].encode('utf-8')

        fields_id = item['rowItem']['sqlfields'].split(',')
        updatesql_fields = item['rowItem']['updatesqlfields'].split(',')
        sql = "INSERT INTO js_vods SET "
        data = []
        for i in fields_id:
            if item['rowItem'].has_key(i):
                sql += i + "=%s ,";
                data.append(item['rowItem'][i])

        if item['images']:
            sql += "pic=%s ,";
            data.append(item['images'][0])
        sql = sql.strip(',')

        if item['rowItem'].has_key('exits_item'):
            if item['rowItem']['exits_item'] != False:
                if item['rowItem']['exits_item']['lens'] < len(item['rowItem']['jump_url']) - 10:
                    update_sql = "UPDATE js_vods SET "
                    update_data = []
                    for i in updatesql_fields:
                        if item['rowItem'].has_key(i):
                            update_sql += i + "=%s ,";
                            update_data.append(item['rowItem'][i])
                    update_sql = update_sql.strip(',') + " WHERE id=%s"
                    update_data.append(item['rowItem']['exits_item']['id'])

                    DB.init().update(update_sql, update_data)
            else:
                DB.init().insertOne(sql,data)
        else:
            DB.init().insertOne(sql,data)
        #print item
        return item


#coding=utf-8
__author__ = 'ShengYue'
import time
import sys,os,json,re
from kan360.common.db import *
from scrapy.selector import Selector
from kan360.common.parser import *
from kan360.common.db import *
reload(sys)
sys.setdefaultencoding('utf8')

domain = '360kan_mv'
html = file(sys.path[0]+'/html/'+domain+'.html', 'a+').read()
hsl = Selector(text=html)

str_xml = file( sys.path[0]+'/../websites/'+domain+'.xml','a+').read()
xsl = Selector(text=str_xml, type='xml')



item = test_parser()
items = item.run(text=html, xml=xsl)


for i in items['rowItem']:
    if type(items['rowItem'][i]) == unicode or type(items['rowItem'][i]) == str:
         items['rowItem'][i] = items['rowItem'][i].encode('utf-8')


print items
# if item['rowItem']:
#     if item['goods']['price'] != item['price'] or item['goods']['original_price'] != item['originalPrice'] or item['goods']['name'] != item['name']:
#         DB.init().update("UPDATE le_goods SET isshow=1,name=%s,price=%s,original_price=%s, uptime=%s,expiry_time=%s,site_id=%s,cate_id=%s WHERE goods_id=%s",[item['name'],item['price'],item['originalPrice'],int(time.time()),item['ExpiryTime'], item['site_id'],goods_cate_id,item['goods']['goods_id']])
#     else:
#         DB.init().update("UPDATE le_goods SET isshow=1,uptime=%s,expiry_time=%s,site_id=%s WHERE goods_id=%s",[int(time.time()),item['ExpiryTime'], item['site_id'],goods_cate_id,item['goods']['goods_id']])
#     DB.init().end()
# else:
#print items
fields_id = items['rowItem']['sqlfields'].split(',')
sql = "INSERT INTO js_vods SET "
data = []
for i in fields_id:
    if items['rowItem'].has_key(i):
        # if items['rowItem'][i] == '':
        #     items['rowItem'][i] = ' '
        sql += i+"=%s ,";
        data.append(items['rowItem'][i])
sql = sql.strip(',')
#DB.init().insertOne(sql,data)
#print items
for i in data:
    print type(i), i




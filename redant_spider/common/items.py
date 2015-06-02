# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BaseItem(Item):
    rowItem = Field()

    # 系统自动图片下载处理
    image_urls = Field()
    images = Field()

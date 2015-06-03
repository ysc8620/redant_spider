# -*- coding: utf-8 -*-

# Scrapy settings for kan360 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kan360'

SPIDER_MODULES = ['kan360.spiders']
NEWSPIDER_MODULE = 'kan360.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kan360 (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    #默认图片下载器关闭
    #'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    #定制图片下载器
    'kan360.common.imagepipelines.MyImagesPipeline': 1,
    #详情图片下载器 针对不需要缩略图
    #'spider.imagepipelines.MyImgPipeline':1,
    #SG处理
    'kan360.common.pipelines.BasePipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
}
# 图片下载保存目录
IMAGES_STORE = '/wwwroot/dir'
# 限速 RANDOMIZE_DOWNLOAD_DELAY 结合随机（0.5 ~ 1.5）* 0.8
DOWNLOAD_DELAY = 0.8


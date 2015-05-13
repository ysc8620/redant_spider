# -*- coding: utf-8 -*-

# Scrapy settings for redant_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'redant_spider'

SPIDER_MODULES = ['redant_spider.spiders']
NEWSPIDER_MODULE = 'redant_spider.spiders'

# 指定
ITEM_PIPELINES = {
    #默认图片下载器关闭
    #'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    #定制图片下载器
    'redant_spider.common.imagepipelines.MyImagesPipeline': 1,
    #详情图片下载器 针对不需要缩略图
    #'spider.imagepipelines.MyImgPipeline':1,
    #SG处理
    'redant_spider.common.pipelines.BasePipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}
# 图片下载保存目录
IMAGES_STORE = '/wwwroot/dir/uploaded'
#缩略图规格及目录名称
IMAGES_THUMBS = {
    'thumb100': (100, 100),
    'thumb250': (250, 250),
    'thumb400': (400, 300),
}
# 限速 RANDOMIZE_DOWNLOAD_DELAY 结合随机（0.5 ~ 1.5）* 0.8
DOWNLOAD_DELAY = 0.8

# 爬虫访问头信息
DOWNLOADER_MIDDLEWARES = {
    # 关闭默认
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    # 使用新定义
    'redant_spider.common.rotate_useragent.RotateUserAgentMiddleware' :400
}

# 以下是scrapy redis 配置
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True

# Schedule requests using a priority queue. (default)
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# Schedule requests using a queue (FIFO).
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

# Schedule requests using a stack (LIFO).
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

# 深度优先下载 默认关闭
# DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

# Max idle time to prevent the spider from being closed when distributed crawling.
# This only works if queue class is SpiderQueue or SpiderStack,
# and may also block the same time when your spider start at the first time (because the queue is empty).
SCHEDULER_IDLE_BEFORE_CLOSE = 10


# redis 服务器配置
# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# 日志
#LOG_FILE = "./error.log"

# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
# 通过链接方式访问
#REDIS_URL = 'redis://user:pass@hostname:9001'
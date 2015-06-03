#-*-coding:utf-8-*-

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
import hashlib
import time,binascii
from base import *
## dd/mm/yyyy格式
#print (time.strftime("%d/%m/%Y"))

class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        #image_guid = request.url.split('/')[-1]
        #image_guid = hashlib.sha1(request.url).hexdigest()
        image_guid = str(binascii.crc32(request.url)).replace('-','0')
        path = image_guid[0:2]
        #date('is',time()) . tools_range::mackcode(3,'NS'). '.' . $ext;
        #time.time()
        return '%s/%s/%s/%s.jpg' % (time.strftime("%Y"),time.strftime("%m%d"), path,image_guid)

    # 缩略图路径
    def thumb_path(self, request, thumb_id, response=None, info=None):
        #image_guid = hashlib.sha1(request.url).hexdigest()
        image_guid = str(binascii.crc32(request.url)).replace('-','0')
        path = image_guid[0:2] #thumbs
        #return 'full/%s%s.jpg' % (path, image_guid)
        #thumb_guid = hashlib.sha1(request.url).hexdigest()  # change to request.url after deprecation
        return '%s/%s/%s/%s/%s.jpg' % (time.strftime("%Y"),time.strftime("%m%d"),thumb_id,path,image_guid)

    def get_media_requests(self, item, info):
        try:
            for image_url in item['image_urls']:
                yield Request(image_url)
        except Exception, e:
            print e
            pass

    def item_completed(self, results, item, info):
        try:
            image_paths = [x['path'] for ok, x in results if ok]
            if not image_paths:
                raise DropItem("Item contains no images")
            item['images'] = image_paths
        except:
            pass
        return item

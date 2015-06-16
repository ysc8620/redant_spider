#-*-coding:utf-8-*-

from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
import hashlib
import time,binascii
## dd/mm/yyyy格式
#print (time.strftime("%d/%m/%Y"))

class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        #image_guid = hashlib.sha1(request.url).hexdigest()
        image_guid = str(binascii.crc32(request.url)).replace('-','0')
        path = image_guid[0:2]
        path1 = image_guid[2:4]
        path2 = image_guid[4:6]
        #date('is',time()) . tools_range::mackcode(3,'NS'). '.' . $ext;
        #time.time()
        return '%s/%s/%s.jpg' % (path,path1,path2, image_guid)

    # 缩略图路径
    def thumb_path(self, request, thumb_id, response=None, info=None):
        #image_guid = hashlib.sha1(request.url).hexdigest()
        image_guid = str(binascii.crc32(request.url)).replace('-','0')
        path = image_guid[0:2] #thumbs
        path1 = image_guid[2:4]
        path2 = image_guid[4:6]
        #return 'full/%s%s.jpg' % (path, image_guid)
        #thumb_guid = hashlib.sha1(request.url).hexdigest()  # change to request.url after deprecation
        return '%s/%s/%s/%s/%s.jpg' % (path,path1,path2,thumb_id,image_guid)

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

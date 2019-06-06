# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import traceback
import uuid

import happybase
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import MydbUtils


class DouBanPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x,meta={'item':item}) for x in item.get(self.images_urls_field,[])]
    def file_path(self, request, response=None, info=None):
        return request.meta['item']['image_store']+'/'+str(uuid.uuid4())+'.jpg'
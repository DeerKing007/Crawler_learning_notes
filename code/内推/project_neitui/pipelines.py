# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import jieba
import jieba.analyse as ja
from scrapy.exceptions import DropItem
import com.project_neitui.project_neitui.settings as settings
import happybase
from uuid import uuid1


class ProjectNeituiPipeline(object):
    # def open_spider(self,spider):
    #     self.connection= happybase.Connection(host='172.16.13.32',port=9090)
    #     self.connection.open()
    #     self.table = self.connection.table('ssss:zp_neitui')
    #
    # def process_item(self, item, spider):
    #     jobName = item['jobName']
    #     salary=item['salary']
    #     companyName=item['companyName']
    #     baseReq=item['baseReq']
    #     jobReq=item['jobReq']
    #     addr=item['addr']
    #     info=item['info']
    #
    #     rowkey=str(uuid1())
    #     self.table.put(rowkey,{'jobinfo:jobName': jobName,'jobinfo:salary': salary,'jobinfo:companyName':companyName,'jobinfo:baseReq':baseReq,'jobinfo:jobReq':jobReq,'jobinfo:addr':addr,'jobinfo:info':info})
    #
    # def close_spider(self,spider):
    #     self.connection.close()

    def process_item(self, item, spider):
        with open('log.txt', 'a+') as w:
            w.write(item['companyName'] + '\n')





 # 去重
class DeleteRepatPipeLine:
    def __init__(self):
        self.temp = set()

    def process_item(self, item, spider):
        s = item['jobName'] + item['salary'] + item['companyName']
        if s in self.temp:
            # pass
            raise DropItem('该item已存在')  # raise   主动抛出
        else:
            self.temp.add(s)
            return item

  # 清洗
class DataCleanPipline:
    def process_item(self, item, spider):
        for i in item:
            item[i].strip()
            # 去除所有不需要的代码
        item['info'] = ','.join(ja.extract_tags(item['info'], topK=10))
        item['jobReq'] = ','.join(ja.extract_tags(item['jobReq'], topK=10))
        return item




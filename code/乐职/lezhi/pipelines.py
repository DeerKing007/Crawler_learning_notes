# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import uuid
import happybase
class DeleteRepatPipeLine:
    def __init__(self):
        self.temp=set()
        def process_item(self, item, spider):
            s=item['name']+item['jobname']+item['education']+item['age']+item['sex']+item['hope_place']
            if s in self.temp:
                raise Exception
            else:
                self.temp.add(s)
            return item
class LezhiPipeline(object):
    def __init__(self,host,port):
        self.host=host
        self.port=port

    def process_item(self, item, spider):
        table=self.connection.table('ssss:lzh_lzjob')
        s = uuid.uuid4()
        # hbase put 'baizhi125:user',"rowkey","base:name","suns"
        table.put('%s' % s, {"f1:name": item['name']})
        table.put('%s' % s, {"f1:sex": item['sex']})
        table.put('%s' % s, {"f1:education": item['education']})
        table.put('%s' % s, {"f1:age": item['age']})
        table.put('%s' % s, {"f1:work_experience": item['work_experience']})
        table.put('%s' % s, {"f1:person_information": item['person_information']})
        table.put('%s' % s, {"f2:jobname": item['jobname']})
        table.put('%s' % s, {"f2:hope_place": item['hope_place']})
        table.put('%s' % s, {"f2:hope_salary": item['hope_salary']})
        table.put('%s' % s, {"f2:now_status": item['now_status']})
    def open_spider(self,spider):
       self.connection = happybase.Connection(host=self.host, port=self.port)
       self.connection.open()
        # spider关闭时被调用---关闭数据库
    def close_spider(self,spider):
        pass
        # 创建pipeline对象之前调用
        #  引擎会自动调用该方法，且是第一个调用该方法---创建pipeline对象
    @classmethod
    def from_crawler(cls,crawler):
        return cls(host='172.16.13.177', port=9090)


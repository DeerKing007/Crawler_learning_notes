# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import happybase

from ai145.jjw.finaljob.finaljob.items import JobItem,resume58Item


class JobPipeline(object):#这里只设置储存到Hbase里，就不设置去重，清洗数据，留给与大数据清洗
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.rowkeyDJ = 1
        self.rowkey58R = 1
    # spider开启时被调用--开启数据库
    def open_spider(self, spider):
        self.connection = happybase.Connection(host=self.host, port=self.port)
        self.connection.open()
    def close_spider(self, spider):
        self.connection.close()
    def process_item(self, item, spider):
        if isinstance(item,JobItem):
            self.table=self.connection.table("baizhizhaopin:daJieZhaoPin")#获取对应表对象（招聘页）
            self.table.put(str(self.rowkeyDJ),{"display:positionName":item["positionName"]})
            self.table.put(str(self.rowkeyDJ),{"display:companyName":item["companyName"]})
            self.table.put(str(self.rowkeyDJ),{"display:salary":item["salary"]})
            self.table.put(str(self.rowkeyDJ),{"display:pproperty":item["pproperty"]})
            self.table.put(str(self.rowkeyDJ),{"display:experience":item["experience"]})
            self.table.put(str(self.rowkeyDJ),{"display:certificate":item["certificate"]})
            self.table.put(str(self.rowkeyDJ),{"display:location":item["location"]})
            self.table.put(str(self.rowkeyDJ),{"hide:city":item["city"]})
            self.table.put(str(self.rowkeyDJ),{"hide:quantity":item["quantity"]})
            self.table.put(str(self.rowkeyDJ),{"hide:scale":item["scale"]})
            self.table.put(str(self.rowkeyDJ),{"hide:industry":item["industry"]})
            self.table.put(str(self.rowkeyDJ),{"hide:comCharacter":item["comCharacter"]})
            self.table.put(str(self.rowkeyDJ),{"hide:officialLink":item["officialLink"]})
            self.table.put(str(self.rowkeyDJ),{"hide:comDesc":item["comDesc"]})
            self.rowkeyDJ+=1
            print("招聘信息入库成功")
            return item

        elif isinstance(item,resume58Item):
            self.table=self.connection.table("baizhizhaopin:5888888888888888888888888888888")#获取对应表对象（简历页）
            self.table.put(str(self.rowkey58R),{"display:name":item['name']})
            self.table.put(str(self.rowkey58R),{"display:gender":item["gender"]})
            self.table.put(str(self.rowkey58R),{"display:age":item["age"]})
            self.table.put(str(self.rowkey58R),{"display:certificate":item["certificate"]})
            self.table.put(str(self.rowkey58R),{"display:experience":item["experience"]})
            self.table.put(str(self.rowkey58R),{"display:hometown":item["hometown"]})
            self.table.put(str(self.rowkey58R),{"display:currentLiving":item["currentLiving"]})
            self.table.put(str(self.rowkey58R),{"display:jobStatus":item["jobStatus"]})
            self.table.put(str(self.rowkey58R),{"display:jobExpect":item["jobExpect"]})
            self.table.put(str(self.rowkey58R),{"display:expectLocation":item["expectLocation"]})
            self.table.put(str(self.rowkey58R),{"display:expectSalary":item["expectSalary"]})
            self.rowkey58R+=1
            print("简历入库成功")
            return item
    @classmethod
    def from_crawler(cls, crawler):#接口函数
        return cls(host=crawler.settings.get("MyHost", '192.168.0.201'),
                   port=crawler.settings.get("Port", 9090))

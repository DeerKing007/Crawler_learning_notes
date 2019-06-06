# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from uuid import uuid1

import MySQLdb


class BossPipeline(object):
    def __init__(self,host,port,user,password,db,charset):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    def open_spider(self,spider):
        print("连接数据库....")
        self.conn = MySQLdb.Connection(host=self.host,port=self.port,user=self.user,password=self.password,db=self.db,charset=self.charset)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        print("数据开始入库.......")
        self.cursor.execute('insert into positionsinfo (position,company,salary,requirements,experience,education,address,department) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',[item['position'],item['company'],item['salary'],item['requirements'],item['experience'],item['education'],item['address'],item['department']])
        self.conn.commit()
        print("数据入库成功！")

    def close_spider(self,spider):
        print("关闭与数据库的连接")
        self.cursor.close()
        self.conn.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host='localhost', port=3306, user='root', password='123456', db='crawler', charset='utf8')

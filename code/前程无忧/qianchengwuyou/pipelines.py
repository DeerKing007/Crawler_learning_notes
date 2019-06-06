# -*- coding: utf-8 -*-
import happybase
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import jieba.analyse as jieba
from scrapy.exceptions import DropItem
import MySQLdb

class QianchengwuyouPipeline(object):


    def process_item(self, item, spider):
        print(item)
        sql=('insert into qcwy_job (job_name,job_salary,job_experience,job_stady,\
                          job_addr,job_info,company_info,company_nature,company_scale,company,\
                          job,addr,company_name,person) values(%s,\
                          %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
        self.cousor.execute(sql,[item['job_name'],item['job_salary'],item['job_experience'], \
                                 item['job_stady'],item['job_addr'][5:], \
                                 item['job_info'],item['company_info'], \
                                 item['company_nature'],item['company_scale'], \
                                 item['company'],int(item['job']),int(item['addr']),item['company_name'],\
                                                                      item['person']])

        self.conn.commit()
    def open_spider(self,spider):
        self.conn = MySQLdb.Connection(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            db='qcwy',
            charset='utf8'
        )
        self.cousor=self.conn.cursor()

    def close_spider(self,spider):
        self.cousor.close()
        self.conn.close()




class De_Weight:#去重
    def __init__(self):
        self.temp=set()
    def process_item(self,item,spider):
        s=item['job_name']+item['job_salary']+item['company']
        if s in self.temp:
            raise DropItem('该数据已存在')
        else:
            self.temp.add(s)
            return item





class FilterPipline:#清洗1
    def process_item(self,item,spider):
       for i in item:
           l=re.findall('\S',item[i])
           item[i]=''.join(l)
       return item



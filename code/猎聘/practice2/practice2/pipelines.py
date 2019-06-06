# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import happybase
from uuid import uuid1


class Practice2Pipeline(object):
    def open_spider(self, spider):
        self.conn = happybase.Connection(host='192.168.142.151', port=9090)
        self.conn.open()
        # self.table1 = self.conn.table('practice2:liepinjob')
        self.table2 = self.conn.table('practice2:zhaopingou')
    #     # self.table3 = self.conn.table('practice2:liepinjob')

    def process_item(self, item, spider):
        if spider.name == 'iron':
            rowkey = str(uuid1())
            # self.table1.put(row=rowkey, data={'jobinfo:jobName': item['jobName']})
            # self.table1.put(row=rowkey, data={'jobinfo:compName': item['compName']})
            # self.table1.put(row=rowkey, data={'jobinfo:salary': item['salary']})
            # # self.table1.put(row=rowkey, data={'jobrequire:detailedReq': item['detailedReq']})
            # self.table1.put(row=rowkey, data={'jobinfo:experience': item['experience']})
            # self.table1.put(row=rowkey, data={'jobinfo:degree': item['degree']})
            # self.table1.put(row=rowkey, data={'jobinfo:compAddr': item['compAddr']})
            # self.table1.put(row=rowkey, data={'jobinfo:department': item['department']})
        elif spider.name == 'black':
            rowkey = str(uuid1())
            datas = {
                'basicinfo:name': item['name'],
                'basicinfo:gender': item['gender'],
                'basicinfo:age': item['age'],
                'basicinfo:birthday': item['birthday'],
                'basicinfo:degree': item['degree'],
                'basicinfo:nationality': item['nationality'],
                'basicinfo:zzmm': item['zzmm'],
                'basicinfo:experience': item['experience'],
                'basicinfo:current_residence': item['current_residence'],
                'basicinfo:household_register': item['household_register'],
                'jobinfo:work_status': item['work_status'],
                'jobinfo:work_addr': item['work_addr'],
                'jobinfo:except_job': item['except_job'],
                'jobinfo:job_info': item['job_info'],
                'jobinfo:except_industry': item['except_industry'],
                'jobinfo:except_salary': item['except_salary']
            }
            self.table2.put(row=rowkey, data=datas)

        elif spider.name == 'fire':
            pass

    def close_spider(self, spider):
        self.conn.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/24 18:26
# @Author  : wjl
# @Site    : 
# @File    : 百合网.py
# @Software: PyCharm

import requests
from lxml import etree
import MySQLdb
#*************************************************************
#建立数据库链接
tuple1=''
def conn_mysql():
    conn = MySQLdb.Connection(host='localhost',
                              port=3306,
                              user='root',
                              password='123456',
                              db='test',
                              charset='utf8'
                              )
    cursor = conn.cursor()
    global tuple1
    tuple1=(conn,cursor)
    print(tuple1)

#存数据,并取数据
def db_save(url):
    conn = tuple1[0]
    cursor = tuple1[1]
    sql1 = 'insert into user_url(url,status) VALUES (%s,%s)'
    count=cursor.execute(sql1,(url,0))
    conn.commit()

#查询数据库：
def query_mysql():
    conn = tuple1[0]
    cursor =tuple1[1]
    sql2='select url from user_url where status=0 limit 0,1'
    cursor.execute(sql2)
    try:
        result = cursor.fetchone()[0]
        print('查询结果是：',result)
        sql3 = 'update user_url set status=%s where url=%s'
        cursor.execute(sql3,(1,result))
        conn.commit()
    except:
        result=''
    print(result,'结果是：')
    return result

#*************************************************************
#发送请求
def send_request(url):
    res = requests.get(url=url).text
    return res
#*************************************************************
#解析url
def anasysis_url(res):
    # 获取用户id
    ele = etree.HTML(res)
    urls = ele.xpath('//div[@class="picList"]/div/ul/li/a/@href')
    return urls
# *************************************************************
#解析详情页
def anasysis_detail(res):
    ele = etree.HTML(res)
    username = ele.xpath('//div[@class="profileTopRight"]/div/span[2]/text()')[0]
    age = ele.xpath('//div[@class="dataH"]/div[1]/p/text()')
    return username, age
#**********************************************************************
#测试
if __name__ == '__main__':
    conn_mysql()
    while 1:
        url=query_mysql()
        if url:
            res = send_request(url)
            urls = anasysis_url(res)
            for url in urls:
                print('开始存储', url)
                try:
                    db_save(url)
                except:
                    pass
                print('存储完毕')
            detail_res=send_request(url)
            print(anasysis_detail(detail_res))
        else:
            break






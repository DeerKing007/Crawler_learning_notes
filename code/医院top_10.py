import requests
from tools.tool import analysisByEqual
from lxml import etree
import pymysql



conn=pymysql.connect(host='localhost',database='spiders',port=3306,user='root',password='123456',charset ='utf8')
cursor=conn.cursor()
sql='insert into hospital_rank values (%s,%s,%s,%s,%s,%s)'


url='http://www.fudanmed.com/institute/news2017-3.aspx'
cookies=analysisByEqual('acw_tc=76b20f6215513247110337305e70fe2e25264d71a03bb699bbf3ff34a9e5c5; HN_WebAdmin=institute_counter=4962707')
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

req=requests.get(url=url,cookies=cookies,headers=headers).text

html=etree.HTML(req)

fenlei=html.xpath('//*[@id="table10"]')[0].xpath('//table')[2].xpath('//tr[@height="45"]|//tr[@height="44"]|//tr[@height="33"]')

for j in range(40):
    temp = fenlei[j*11:(j+1)*11]
    # print(j*12,(j+1)*12)
    if temp:
        kind=temp[0].xpath('./td[1]/text()')[0].strip()
        print(kind)
        for i in temp[1:]:
            td1 = i.xpath('./td[1]/text()')[0].strip()
            td2 = i.xpath('./td[2]/text()')[0].strip()
            td3 = i.xpath('./td[3]/text()')[0].strip()
            td4 = i.xpath('./td[4]/text()')[0].strip()
            td5 = i.xpath('./td[5]/text()')[0].strip()
            cursor.execute(sql,[kind,td1,td2,td3,td4,td5,])

conn.commit()
# 关闭光标对象
cursor.close()
# 关闭数据库连接
conn.close()

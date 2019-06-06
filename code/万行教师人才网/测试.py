import time

import requests
import com.baizhi.AI145.后期项目.utils.解析为字典的工具 as tools
from lxml import etree

pageIndex=1
while 1:
    url = 'http://www.job910.com/search.aspx?funtype=&salary=&maxSalary=&minSalary=&workMethod=&sortField=1&education=&experience=&uptime=&area=&keyword=%E6%95%B0%E5%AD%A6&sort=0&pageSize=20&pageIndex=' + str(pageIndex)
    # print(result)
    # e_html = etree.HTML(result)
    list_page=requests.get(url).text
    # print('requests.get(url)',requests.get(url),type(requests.get(url)))
    # print('requests.get(url).text',list_page,type(list_page))
    e_html = etree.HTML(list_page)
    # print('etree.HTML(list_page)',e_html,type(e_html))
    detail_urls=[]
    for i in e_html.xpath('//ul[@class="search-result-list"]/li/div[@class="info-col-1st"]/div[@class="position title"]/a/@href'):
        detail_url = 'http://www.job910.com' + i
        detail_urls.append(detail_url)
    if detail_urls==[]:
        print('pageIndex', pageIndex)
        break
    print(detail_urls)
    print('pageIndex',pageIndex)
    pageIndex+=1





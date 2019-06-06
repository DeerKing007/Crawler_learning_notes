import json
from lxml import etree

import chardet
import requests
'''
中国人才热线
'''


def sendRequest():
    res = requests.post(url=url, data=data)
    res.encoding = chardet.detect(res.content)['encoding']
    sjson = json.loads(res.text)
    shtml = sjson['JobListHtml']
    return shtml


def parse_Urllist(shtml):
    html = etree.HTML(shtml)
    urllist = html.xpath('//ul[@class="results_list_box"]/li[2]/h3/a/@href')
    return urllist


def parse_Data(urls):
    for i in urls:
        try:
            res = requests.get(url=i,timeout=2).text
            html = etree.HTML(res)
            title = html.xpath('//div[@class="jname-jobintro"]/text()')
            title1 = ''.join(title)
            money = html.xpath('//ul[@class="require-jobintro clearfix"]/li/em/text()')
            money1 = ''.join(money)
            times = html.xpath('//div[@class="pubtime-jobintro f_l"]/text()')
            times1 = ''.join(times)
            print(title1,money1,times1)
        except:
            print('访问超时,过滤...')

if __name__ == '__main__':
    page = 1
    url = 'http://s.cjol.com/service/joblistjson.aspx'
    data = {
        'KeywordType': '3',
        'RecentSelected': '43',
        'SearchType': '1',
        'ListType': '2',
        'page': str(page)
    }
    while 1:
        print('当前页数:',page)
        parse_Data(parse_Urllist(sendRequest()))
        page += 1
        if page >= 999:
            break
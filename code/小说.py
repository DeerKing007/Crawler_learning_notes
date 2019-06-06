import xlwt
import requests
from lxml import etree
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
}

all_info_list = []


def get_info(url):
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="all-img-list cf"]/li')
    for info in infos:
        title = info.xpath('div[2]/h4/a/text()')[0]
        author = info.xpath('div[2]/p[1]/a[1]/text()')[0]
        style1 = info.xpath('div[2]/p[1]/a[2]/text()')[0]
        style2 = info.xpath('div[2]/p[1]/a[3]/text()')[0]
        style = style1 + '.' + style2
        complete = info.xpath('div[2]/p[1]/span/text()')[0]
        introduce = info.xpath('div[2]/p[2]/text()')[0].strip()
        word = info.xpath('div[2]/p[3]/span/span/text()')[0].strip('万字')
        info_list = [title, author, style, complete, introduce, word]
        all_info_list.append(info_list)
    time.sleep(1)


if __name__ == '__main__':
    urls = ['https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page={}'.format(
        str(i)) for i in range(1, 11)]
    page_crawled = 1
    for url in urls:
        get_info(url)
        print("{} pages has crawled".format(str(page_crawled)))
        page_crawled += 1
    header = ['题目', '作者', '类型', '连载状态', '介绍', '字数']
    book = xlwt.Workbook(encoding='utf-8-sig')
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])
    i = 1
    for list in all_info_list:
        j = 0
        for data in list:
            sheet.write(i, j, data)
            j += 1
        i += 1
    book.save('xiaoshuo.xls')

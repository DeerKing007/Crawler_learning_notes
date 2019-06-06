import requests
from lxml import etree


def geturl(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
    xiangqiye = requests.get(url, headers=headers).text
    return xiangqiye


def jiexi(xiangqiye):
    e_html = etree.HTML(xiangqiye)
    name = e_html.xpath('//span[@class="title"]/text()')  # 游戏名
    jiage = e_html.xpath('//div[@class="col search_price  responsive_secondrow"]/text() | //div[@class="col search_price discounted responsive_secondrow"]/text()[2]')
    lianjie = e_html.xpath('//a[@class="search_result_row ds_collapse_flag "]/@href')
    # print(len(name), len(jiage))
    # print(lianjie)
    for i in range(len(name)):
        print(name[i], jiage[i].strip(), lianjie[i])


if __name__ == '__main__':
    a = 1
    while 1:
        url = 'https://store.steampowered.com/search/?filter=topsellers&os=win&page='+str(a)
        a += 1
        jiexi(geturl(url))

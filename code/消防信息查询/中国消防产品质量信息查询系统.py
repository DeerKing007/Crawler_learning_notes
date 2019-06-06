import requests
from com.baizhi.Section.Section_4.utils.str_to_dict import headers_to_dict
from lxml import etree
import json


class Txt:
    def __init__(self):
        self.f = open(file='消防产品.txt', mode='a', encoding='utf-8')
    def save(self, line):
        self.f.write(line)
    def close(self):
        self.f.close()


def createSession():
    headers = headers_to_dict('''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Cookie: JSESSIONID=A0D77C1FD8FAC57C0E8A413F4A9A021C; Hm_lvt_8b09cd1ce77519bec46855c2d4d179a9=1551084523; Hm_lpvt_8b09cd1ce77519bec46855c2d4d179a9=1551084736
DNT: 1
Host: www.cccf.com.cn
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36''')
    session = requests.session()
    session.headers.update(headers)
    return session


# 列表页
def sendList(session, pn):
    url = 'http://www.cccf.com.cn/net/searchProduct.do'
    data = {
        'pageAction': 'nextPage',
        'pages': pn,
        'totalPage': 21522,
        'jumpPage': pn,
        'totalpages': 21522,
        'currentpage': pn,
    }
    return session.post(url=url, data=data)


# 解析列表页
def getUrls(response):
    response.encoding = response.apparent_encoding
    html = etree.HTML(response.text)
    tables = html.xpath('//form/table[3]/tr/td/table/tr[2]/td/table')
    for table in tables:
        yield ''.join(table.xpath('./tr/td[2]/a/text()')).replace('\n', '').strip()


# 发送请求，并解析详情页
def getData(session, goodId):
    url = 'http://www.cccf.net.cn:8001/newoa/enterInfo.jsp'
    params = {'certificateNo': goodId}
    res = session.get(url=url, params=params)
    res.encoding = res.apparent_encoding
    temp = json.loads(res.text.replace('\n', '').strip().strip('null(').strip(')'))
    comp = temp['enterpriseName']
    name = temp['juridicalPerson']
    contactPerson = temp['contactPerson']
    addr = temp['address']
    phone = temp['contactTel']
    return comp+'\t'+name+'\t'+contactPerson+'\t'+addr+'\t'+phone+'\n'


if __name__ == '__main__':
    session = createSession()
    txt = Txt()
    for pn in range(21522):
        res = sendList(session, pn)
        for goodId in getUrls(res):
            data = getData(session, goodId)
            txt.save(data)
        txt.close()
        break

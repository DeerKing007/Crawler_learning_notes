import requests
from lxml import etree
import utils.解析为字典的工具 as tools


def sendurl(url):
    cookies = tools.analysisByEqual("statistics_clientid=me; ganji_xuuid=6bdb6a94-89f2-4f91-ba5a-0b50deec228d.1551097567909; ganji_uuid=8581968077699422875443; SiftRecord['1551097668']=python%3C%E6%B1%82%E8%81%8C%E7%AE%80%E5%8E%86%3E%7C%7C%2Fqiuzhi%2Fs%2F_python%2F; cityDomain=bj; vip_version=new; __utmt=1; GANJISESSID=6gupbamro374ttrs96u8brojli; sscode=QD0o0woAitOlDqWyQDb8jXRD; GanjiUserName=%23qq_806768427; GanjiUserInfo=%7B%22user_id%22%3A806768427%2C%22email%22%3A%22%22%2C%22username%22%3A%22%23qq_806768427%22%2C%22user_name%22%3A%22%23qq_806768427%22%2C%22nickname%22%3A%22%5Cu6175%5Cu61d2%5Cu7684%5Cu6211%5Cu54fc%5Cu7740%5Cu4e0d%5Cu6210%5Cu8c03%5Cu7684%5Cu5c0f%5Cu66f2%22%7D; bizs=%5B%5D; last_name=%23qq_806768427; xxzl_deviceid=NkVNIgIqF3bR2%2FVXYygr1RZjcVNjxLQbhdDw8RKaJv%2FNsWdTJepvC5P72H%2FWRruC; xxzl_smartid=7fb530c67186b09fd9740b46783c8f39; Hm_lvt_8da53a2eb543c124384f1841999dcbb8=1551099951; Hm_lpvt_8da53a2eb543c124384f1841999dcbb8=1551099977; ganji_login_act=1551099977413; Hm_lvt_acb0293cec76b2e30e511701c9bf2390=1551099951; Hm_lpvt_acb0293cec76b2e30e511701c9bf2390=1551099977; lg=1; __utma=32156897.514222813.1551098168.1551098168.1551098168.1; __utmb=32156897.9.10.1551098168; __utmc=32156897; __utmz=32156897.1551098168.1.1.utmcsr=bj.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/qiuzhi/s/_python/; _gl_tracker=%7B%22ca_source%22%3A%22www.baidu.com%22%2C%22ca_name%22%3A%22se%22%2C%22ca_kw%22%3A%22%25E8%25B5%25B6%25E9%259B%2586%7Cutf8%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A73569233960%2C%22kw%22%3A%22python%22%7D; STA_DS=1")
    res = requests.get(url=url, cookies=cookies).text
    return res


def gethtml(html):
    res1 = etree.HTML(html)
    result = res1.xpath('//dt[@class="j-post"]/a/@href')
    return result


def getdetail(url1):
    res1 = sendurl(url1)
    html = etree.HTML(res1)
    try:
        name = html.xpath('//div[@class="name-line"]/strong/text()')[0]
        sex = html.xpath('//div[@class="name-line"]/span/text()')[0]
        age = html.xpath('//div[@class="name-line"]/span[@class="left-border"]/text()')[0]
        print(name, sex, age)
    except:
        name = html.xpath('//span[@class="offer_name"]/text()')[0]
        sex = html.xpath('//span[@class="offer_age"]/text()')[0][1:2]
        age = html.xpath('//span[@class="offer_age"]/text()')[0][3:6]
        print(name, sex, age)
    return name, sex, age


if __name__ == '__main__':
    pn=0
    while pn<=64:
        url = 'http://bj.ganji.com/qiuzhi/s/f%s/_python/' % pn
        print(url)
        pn += 32
        for i in gethtml(sendurl(url)):
            getdetail('http://bj.ganji.com'+i)



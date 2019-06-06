import requests
from lxml import etree

def getRequest(url,headers):
        html = requests.get(url, headers=headers).text
        html = etree.HTML(html)
        xqurl = html.xpath('//div[@data-widget="app/ms_v2/wanted/list.js#companyAjaxBid"]/dl/dt/a/@href')
        return xqurl

def xiangqingPage(url,headers):
        html = requests.get(url,headers=headers).text
        html = etree.HTML(html)
        post_name = html.xpath('//div[@class="title-line clearfix"]/h2/text()')
        post = html.xpath('//div[@class="title-line clearfix"]/p/text()')
        salary = html.xpath('//div[@class="salary-line"]/b/text()')
        post_name = ''.join(post_name)
        post = ''.join(post)
        salary = ''.join(salary)
        print(post_name,post,salary)



if __name__ == '__main__':
        page = 1
        while 1:
                # url = 'http://bj.ganji.com/site/s/_Python/'
                # url = 'http://bj.ganji.com/zp   sqgongchengshi/'
                url = 'http://bj.ganji.com/zpshichangyingxiao/o%s/' % page
                headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
                }
                html_url = getRequest(url=url,headers=headers)
                for i in html_url:
                     xiangqingPage(url=i,headers=headers)
                page+=1
                if not html_url:
                        break









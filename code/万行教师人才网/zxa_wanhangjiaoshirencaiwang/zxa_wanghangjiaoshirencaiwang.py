import requests
from lxml import etree
import utils.解析为字典的工具 as tools
import zpg_job_information.zpg_job_information as zpg


class UrlListTools(zpg.UrlListTools):
    #解析列表页中详情页的url
    def analysisUrls(self,url,**kwargs):
        data=self.sendRequest(url,**kwargs)
        e_html=etree.HTML(data)
        detail_urls = []
        for i in e_html.xpath('//ul[@class="search-result-list"]/li/div[@class="info-col-1st"]/div[@class="position title"]/a/@href'):
            detail_url = 'http://www.job910.com' + i
            detail_urls.append(detail_url)
        return detail_urls

class DetailTools:
    #解析详情页数据
    def analysisData(self,urls):
        for url in urls:
            e_html=etree.HTML(requests.get(url).text)#element对象
            try:
                job_name=e_html.xpath('//div[@class="job-name"]/span/text()')[0].strip()
                company_name=e_html.xpath('//div[@class="job-name"]/div/a/text()')[0]
            except:
                print('模板一失效！')
            yield [job_name,company_name,keywordIndex,areaIndex,pageIndex]

class DatabaseTools(zpg.DatabaseTools):
    pass

def main(url,keyword=[],area=[],keywordIndex=0,areaIndex=0,pageIndex=1):
    #主运行程序
    while 1:
        data="""
        funtype: 
        sortField: 1
        sort: 1
        pageSize: 20
        pageIndex: %s
        salary: 
        maxSalary: 
        minSalary: 
        workMethod: 
        education: 
        experience: 
        uptime: 0
        keyword: %s
        area: %s
        """%(pageIndex,keyword[keywordIndex],area[areaIndex])
        detail_urls=UrlListTools().getUrls(url)
        if detail_urls == []:
            #判断成功说明该keyword和area下的所有页码都爬取完了，更换keyword
            if keywordIndex == len(keyword)-1:
                #判断成功更换area
                if areaIndex==len(area)-1:
                    break
                else:
                    areaIndex+=1
            else:
                keywordIndex+=1
        # for i in DetailTools().analysisData(detail_urls):
        #     #i为数据，要保存到数据库
        #     dbTools.saveDB(i,'wanhang')
        print('pageIndex', pageIndex,detail_urls)
        pageIndex+=1


if __name__ == '__main__':
    # dbTools=DatabaseTools.dbFrom()
    keyword=['语文','数学','英语']
    area=[110000,310000,130000,410000]#北京，上海，河北，河南
    keywordIndex,areaIndex=0,0
    pageIndex=1
    url = 'http://www.job910.com/search.aspx'

    main(url,keyword=keyword,area=area,keywordIndex=keywordIndex,areaIndex=areaIndex,pageIndex=pageIndex)


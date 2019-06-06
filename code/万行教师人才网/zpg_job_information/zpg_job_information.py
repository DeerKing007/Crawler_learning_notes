import requests
from lxml import etree
import json
import MySQLdb
import utils.解析为字典的工具 as tools


#获取列表页的工具
class UrlListTools:
    def __init__(self):
        pass

    #发送请求
    @staticmethod
    def sendRequest(url,requestType='get',data={},params={},headers={},cookies={},proxies={},**kwargs):
        res=requests.request(requestType,url,data=data,params=params,headers=headers,cookies=cookies,proxies=proxies,**kwargs)
        res.encoding=res.apparent_encoding
        return res.text

    #解析列表页中的详情url
    def analysisUrls(self,url,**kwargs):
        data=self.sendRequest(url,**kwargs)
        print('+++++++++++++++++',data)
        rData=json.loads(data)
        return ['http://www.zhaopingou.com/jobs/'+str(i['id'])+'.html' for i in rData['positionReleaseList']]

    #对外提供调用接口---解耦合
    def getUrls(self,url,**kwargs):
        return self.analysisUrls(url,**kwargs)


class DetailTools:
    # @staticmethod
    def analysisData(self,urls,keyIndex=0,cityIndex=0,pageSize=1,**kwargs):
        for url in urls:
            #发送请求并初始化
            e_html=etree.HTML(requests.get(url,**kwargs).text)
            #解析html，第一套模板
            try:
                #公司名称
                company_name = e_html.xpath('//h2[@id="position_detail_id"]/text()')[0]
            except:
                company_name = ''
            try:
                #职位名称
                job_name = e_html.xpath('//p[@class="le public-howa760 position_name"]/text()')[0]
            except:
                job_name=''
            try:
                #薪资
                salary = e_html.xpath('//h2[@class="clearfloat"]/span/text()')[0]
            except:
                salary=''
            try:
                #公司地址
                company_addr = e_html.xpath('//ul[@class="comp-resume-msg le"]/li[1]/text()')[0]
            except:
                company_addr=''
            try:
                #工作性质
                job_nature = e_html.xpath('//ul[@class="comp-resume-msg le"]/li[2]/text()')[0]
            except:
                job_nature=''
            try:
                #工作分类
                job_classification = e_html.xpath('//ul[@class="comp-resume-msg le"]/li[3]/text()')[0]
            except:
                job_classification=''
            try:
                #学历
                education_background = e_html.xpath('//ul[@class="comp-resume-msg le"]/li[4]/text()')[0]
            except:
                education_background=''
            try:
                #经验
                experience = e_html.xpath('//ul[@class="comp-resume-msg le"]/li[5]/text()')[0]
            except:
                experience=''
            try:
                #职位描述
                job_description_list = e_html.xpath('//div[@class="form-edit-conten need-lietou-dashed"]/p/text()')
                job_description = ''
                for i in job_description_list:
                    job_description += i.replace('\xa0', '')
            except:
                job_description=''
            try:
                #公司网址
                company_websites = e_html.xpath('//div[@class="compant-msg-list"]/p[1]/a/span/text()')[0]
            except:
                company_websites=''
            try:
                #职位标签
                position_lables = e_html.xpath('//div[@class="compant-msg-list"]/p[2]/span/text()')[0]
            except:
                position_lables=''
            if company_name=='' and job_name=='' and salary=='' and company_addr=='' and job_nature=='' and job_classification=='' and education_background=='' and experience=='' and job_description=='' and company_websites=='' and position_lables=='':
                #第二套模板
                print('第一套模板失效！请更换模板')
            yield [company_name,job_name,salary,company_addr,job_nature,job_classification,education_background,experience,job_description,company_websites,position_lables,keyIndex,cityIndex,pageSize]


class DatabaseTools:
    def __init__(self, host, port, user, password, db, charset):
        self.conn = MySQLdb.Connection(host=host, port=port, user=user, password=password, db=db, charset=charset)
        self.cursor = self.conn.cursor()

    def saveDB(self, data, tableName):
        n = len(data)
        print(n)
        sql = 'insert into ' + tableName + ' values(' + ('%s,'*n)[:-1] + ')'
        self.cursor.execute(sql, data)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    @classmethod
    def dbFrom(cls,host='localhost',port=3306,user='root',password='123456',db='last_item',charset='utf8'):
        # 可以做前置工作，并且不需要消耗当前对象资源
        # 类方法不需要创建实例对象就可以使用
        return cls(host=host,port=port,user=user,password=password,db=db,charset=charset)


def main(cityId=[],key=[],url='',cookies={},cityIndex=0,keyIndex=0,pageSize=0,tableName='zpg_job_information',**kwargs):
    while 1:
        data=tools.analysisByColon("""
        cityId: %s
        addressQu: 
        strKey: %s
        workYears: 
        degreesTypes: 
        positionNature: 
        companyNature: 
        companyScaleId: 
        companySeedtime: 
        monthType: 
        monthStr: 
        sPayMonth: 
        ePayMonth: 
        pageSize: %s
        pageNo: 25
        clientNo: 
        userToken: 
        clientType: 2
        """%(cityId[cityIndex],key[keyIndex],pageSize))
        listUrls=UrlListTools().getUrls(url,cookies=cookies,data=data,**kwargs)
        print("UUUUUUUUUUUUUUUU",listUrls)
        detailDatas=DetailTools().analysisData(listUrls,keyIndex=keyIndex,cityIndex=cityIndex,pageSize=pageSize) # 是个生成器：是个可迭代对象
        print('66666666666666666',cityIndex,keyIndex,pageSize)
        # for i in detailDatas: # i:每一次的所有数据[jobName,company,salary,requirement,message,desc,companySize,tel]
        #     dbTools.saveDB(i,tableName)
        if len(listUrls) == 0:
            pageSize=0
            # 此时视为该条件已经爬取完毕
            # 更换条件继续查询--本质更换的是下标
            if cityIndex == len(cityId) - 1:  # city已满
                cityIndex = 0
                if keyIndex == len(key) - 1:  # kw已满
                    # 彻底执行完毕
                    # dbTools.close()
                    break
                else:
                    keyIndex += 1
            else:
                cityIndex += 1
        else:
            pageSize+=1


if __name__ == '__main__':
    # dbTools = DatabaseTools.dbFrom()
    url='http://www.zhaopingou.com/zhaopingou_interface/c_search_find_position?timestamp=1550218984819'
    cityId=[1,2,3,5]
    key=['python','web','爬虫','大数据','AI']
    cookies=tools.analysisByEqual("user_account_session=8407d544-ef4f-41d8-9cda-6c2fce7fd92eAAA4; hrkeepToken=5D0533105244C735A6C30C941145EAC5; zhaopingou_account=18830202349; zhaopingou_select_city=1; zhaopingou_zengsong_cookie_newDay=2019-02-18%3D2; zhaopingou_htm_cookie_newDay=2019-02-18; JSESSIONID=9AEB1BC874E2E635E8A16E472AD1ED50; Hm_lvt_b025367b7ecea68f5a43655f7540e177=1550630055,1550632080,1550632625,1550650107; Hm_lpvt_b025367b7ecea68f5a43655f7540e177=1550650139")
    main(cityId=cityId,key=key,keyIndex=0,cityIndex=0,pageSize=0,url=url,cookies=cookies,requestType='post')


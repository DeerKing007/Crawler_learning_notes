# -*- coding: utf-8 -*-

import json
import scrapy
import time

import ai145.jjw.finaljob.finaljob.items as items


class DajieSpider(scrapy.Spider):
    name = 'dajie'
    allowed_domains = ['so.dajie.com/job/search'] # 允许访问的域名---检测
    start_urls = ['http://so.dajie.com/job/search/'] # 入口链接---

    def parse(self, response):#入口函数
        self.cities=['110000','310000','440100','440300']
        self.keyword=['python','web','爬虫','大数据','AI']
        # 入口处初始有三项是1
        self.cityIndex=0
        self.keywordIndex=0
        self.pageNum = 1
        self.token = 'ZTiSscknZ_BxCuTSyx_FRHQZ6xxSmpnOm-hfFTo*'
        self.url='https://so.dajie.com/job/ajax/search/filter?keyword=%s&order=0&city=%s&s&recruitType=&salary=&experience=&page=%s&positionFunction=&_CSRFToken=%s'
        # return scrapy.Request(url=self.url%(self.keyword[self.keywordIndex],self.cities[self.cityIndex],self.pageNum,self.token),callback=self.listParse,dont_filter=True)
        return scrapy.Request(url=self.url%(self.keyword[self.keywordIndex],self.cities[self.cityIndex],self.pageNum,self.token),callback=self.listParse,dont_filter=True)

    def listParse(self,response): #列表页解析方法

        res=scrapy.Selector(response).extract()#讲相应对象转成selector对象
        res=res.strip("<html><body><p>").strip('</p></body></html>')
        res=json.loads(res)#json解析成字典

        while 1:#爬到总页数停止到下一个关键字
            linkList=[]#临时装每页的链接列表
            for each in res["data"]["list"]:#收集所有职位链接
                linkList.append('http:'+each['jobHref'])
            print(linkList)
            for eachLink in linkList:
                time.sleep(0.5)
                yield scrapy.Request(url=eachLink,callback=self.detailParse,dont_filter=True)
            self.pageNum += 1  # 页数+1
            print(self.pageNum)
            print(self.keywordIndex)
            print(self.cityIndex)
            time.sleep(10)

            # 下一列表页回调自己
            yield scrapy.Request(
                url=self.url % (self.keyword[self.keywordIndex], self.cities[self.cityIndex], self.pageNum, self.token),
                callback=self.listParse, dont_filter=True)

            if self.pageNum>res["data"]["totalPage"]:#判断页数够了
                time.sleep(20)
                self.pageNum=1#页数归1
                self.keywordIndex += 1  # 关键字下标+1
                if self.keywordIndex >=len(self.keyword):#是否关键字下标越界
                    time.sleep(20)
                    self.keywordIndex=0#越界后归0
                    self.cityIndex+=1#城市下标+1
                    if self.cityIndex >=len(self.cities):#判断是否城市越界
                        break


        # return scrapy.Request(url='https://job.dajie.com/74c7eaf2-16d4-4e19-86c8-4b41b8643f2e.html?jobsearch=0&pagereferer=blank&keyword=python&clicktype=job', callback=self.detailParse, dont_filter=True)

    def detailParse(self,response):#详情页解析方法
        selector=scrapy.Selector(response)#讲相应对象变为字符串

        pn_and_pproperty=selector.xpath('//div[@class="job-msg-top-text"]/span/text()').extract()
        # 职位名获取
        try:
            positionName=pn_and_pproperty[0]
        except:
            return None
        # 工作性质获取
        try:
            pproperty=pn_and_pproperty[1].strip('（').strip("）")
        except:
            pproperty = "无说明"
        # 工资
        try:
            salary=selector.xpath('//span[@class="job-money"]/text()').extract()[0]
        except:
            salary="面议"

        rreq=selector.xpath('//div[@class="job-msg-center"]//span/text()').extract()# 基本要求
        # 城市名
        try:
            city = rreq[0]
        except:
            return None
        # 招聘人数
        try:
            quantity = rreq[1]
        except:
            quantity = "若干"
        try:
            if len(rreq)==4:#判断职位要求项数
                experience=rreq[2]
                certificate=rreq[3]
            else:
                experience = '无经验要求'
                certificate = rreq[2]
        except:
            experience = '无经验要求'
            certificate = '无学历要求'
        # 公司名
        try:
            companyName=selector.xpath('//p[@class="title"]/*/text()').extract()[0]
        except:
            return None
        try:
            comInfo=selector.xpath('//ul[@class="info"]//span/text()').extract()#公司信息
        except:
            comInfo="-"
        # 公司规模
        try:
            scale=comInfo[0]
        except:
            scale=''
        # 领域
        try:
            industry=comInfo[1]
        except:
            industry=''
        # 公司性质
        try:
            comCharacter=comInfo[2]
        except:
            comCharacter=''
        # 官网
        try:
            officialLink=comInfo[3]
        except:
            officialLink = "————"
        # 公司描述
        try:
            comDesc=selector.xpath('//pre/text()').extract()[0]
        except:
            comDesc='-'
        # 工作地点
        try:
            location=selector.xpath('//div[@class="ads-msg"]/span/text()').extract()[0]
        except:
            location='不明'

        item=items.JobItem()#类字典对象
        item['pproperty']=pproperty#
        item['positionName']=positionName#
        item['salary']=salary#
        item['city']=city
        item['quantity']=quantity
        item['experience']=experience#
        item['certificate']=certificate#
        item['companyName']=companyName#
        item['scale']=scale
        item['industry']=industry
        item['comCharacter']=comCharacter
        item['officialLink']=officialLink
        item['comDesc']=comDesc
        item['location']=location

        return item




# -*- coding: utf-8 -*-
import scrapy
import time
from ..items import QianchengwuyouItem
class QianchengSpider(scrapy.Spider):
    name = 'qiancheng'
    allowed_domains = ['mkt.51job.com/tg/sem/pz_2018.html?from=baidupz']
    start_urls = ['http://mkt.51job.com/tg/sem/pz_2018.html?from=baidupz/']
    def parse(self, response):
        city=[('010000','1'),('020000','2'),('030200','3'),('040000','4')]
        for c in city:
            job = [('python web','1'),('爬虫','2'),('大数据','3'),('AI','4')]
            for j in job:
                url='https://search.51job.com/list/{0},000000,0000,00,9,99,{1},2,1.html'.format(c[0],j[0])
                yield scrapy.Request(meta={'addr':c[1],'job':j[1]},url=url,callback=self.listurl,dont_filter=True,)


    def listurl(self,response):
        res=scrapy.Selector(response)
        html=res.xpath('//p[@class="t1 "]/span/a/@href').extract()
        for i in html:
            # print(i)
            with open(r'E:\Djianggo\re\qianchengwuyou\前程无忧', 'a') as f:
                f.write(i+'\n')
            yield scrapy.Request(meta={'addr':response.meta['addr'],'job':response.meta['job']},url=i,dont_filter=True,callback=self.filter)
        s = res.xpath('//li[@class="bk"]')[1].xpath('./a/@href').extract()
        if s:
            yield scrapy.Request(meta={'addr':response.meta['addr'],'job':response.meta['job']},url=s[0],dont_filter=True,callback=self.listurl)


    def filter(self,response):
        item=QianchengwuyouItem()
        res=scrapy.Selector(response)
        item['job']=response.meta['job']
        item['addr']=response.meta['addr']
        try:
            item['job_name']=res.xpath('//h1/@title').extract()[0]#职位
        except:
            item['job_name']='无'
        try:
            item['job_salary']=res.xpath('//h1/following-sibling::strong[1]/text()').extract()[0]#月薪
        except:
            item['job_salary']='无'
        try:
            item['company_name']=res.xpath('//p[@class="cname"]/a/@title').extract()[0]#公司
        except:
            item['company_name']='无'
        
        job_basic=res.xpath('//p[@class="msg ltype"]/@title').extract()[0]#基本要求
        job_basic=job_basic.split()
        try:
            item['job_experience']=job_basic[2]
        except:
            item['job_experience']='无'
        try:
            item['job_stady']=job_basic[4]
            if '招' in job_basic[4]:
                item['job_stady'] = '无'
        except:
            item['job_stady'] ='无'
        try:
            if '招' in job_basic[6]:
                item['person'] = job_basic[6]
            else:
                item['person']=job_basic[4]
                if '招' not in job_basic[4]:
                    item['person'] ='无'
        except:
            item['person']='无要求'
        try:
            item['job_info']=res.xpath('string(//div[@class="bmsg job_msg inbox"])').extract()[0]#职位信息
        except:
            item['job_info']='无'
        try:
            if res.xpath('string(//div[@class="bmsg inbox"]/p)').extract()[0]==None:
                item['job_addr']='暂无'
            else:
                item['job_addr']=res.xpath('string(//div[@class="bmsg inbox"]/p)').extract()[0]#工作地址

        except:
            item['job_addr']='无'
        try:
            item['company_info']=res.xpath('//div[@class="tmsg inbox"]/text()').extract()[0]#公司信息
        except:
            item['company_info']='无'
        try:
            item['company_nature']=res.xpath('//div[@class="com_tag"]//p[1]/@title').extract()[0]#公司性质
        except:
            item['company_nature']='无'
        try:
            item['company_scale']=res.xpath('//div[@class="com_tag"]//p[2]/@title').extract()[0]#公司规模
        except:
            item['company_scale']='无'
        try:
            item['company']=res.xpath('//div[@class="com_tag"]//p[3]/@title').extract()[0]#公司业务
        except:
            item['company']='无'
        return item



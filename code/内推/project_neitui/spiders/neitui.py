# -*- coding: utf-8 -*-
import scrapy
import com.project_neitui.project_neitui.items as items


class NeituiSpider(scrapy.Spider):
    name = 'neitui'
    allowed_domains = ['www.neitui.me']
    start_urls = ['http://www.neitui.me/']

    def parse(self, response):
        city=['%E5%8C%97%E4%BA%AC','%E4%B8%8A%E6%B5%B7','%E5%B9%BF%E5%B7%9E','%E6%B7%B1%E5%9C%B3']
        keyword=['Python','%E5%A4%A7%E6%95%B0%E6%8D%AE','%E7%88%AC%E8%99%AB','AI']

        for i in city:
            for j in keyword:
                while 1:
                    url='http://www.neitui.me/?name=job&handle=lists&city='+i+'&keyword='+j+'&page=1'
                    yield scrapy.Request(url=url,callback=self.listParse,dont_filter=True)

    def listParse(self,response):
        res=scrapy.Selector(response)
        urls=res.xpath('//div[@class="mt5 clearfix"]/a/@href').extract()
        for i in urls:
            yield scrapy.Request(url='http://www.neitui.me'+str(i),callback=self.detailParse,dont_filter=True)
        nextPage=''.join(res.xpath('//*[@id="ntJobList"]/div/div[1]/div[2]/nav/ul/li[12]/a/@href').extract())
        if nextPage:
            yield scrapy.Request(url='http://www.neitui.me'+str(nextPage),callback=self.detailParse,dont_filter=True)

        # resList=[]
        # res = scrapy.Selector(response)
        # urls = res.xpath('//div[@class="mt5 clearfix"]/a/@href').extract()
        # for i in urls:
        #     resList.append(scrapy.Request(url='http://www.neitui.me' + str(i), callback=self.detailParse, dont_filter=True))
        # nextPage = ''.join(res.xpath('//*[@id="ntJobList"]/div/div[1]/div[2]/nav/ul/li[12]/a/@href').extract())
        # if nextPage:
        #     resList.append(scrapy.Request(url='http://www.neitui.me'+str(nextPage), callback=self.detailParse, dont_filter=True))
        # return resList





    def detailParse(self,response):
        res=scrapy.Selector(response)
        item=items.ProjectNeituiItem()
        item['jobName']=''.join(res.xpath('//div[@class="c333 font26"]/text()').extract())
        item['salary']=''.join(res.xpath('//span[@class="orange mr10"]/text()').extract())
        item['companyName']=''.join(res.xpath('//a[@class="c333 font18"]/text()').extract())
        item['baseReq']=''.join(res.xpath('//div[@class="font16 mt10 mb10"]//span[@class="mr10"]/text()').extract())
        item['jobReq']=''.join(res.xpath('//div[@class="mb20 jobdetailcon"]/text()').extract())
        item['addr']=''.join(res.xpath('//*[@id="jobDetail"]/div[3]/div/div/div[2]/div[3]/text()').extract())
        item['info']=''.join(res.xpath('//div[@class="col-xs-8"]//div//span[@class="grey"]/text()').extract())

        return item

        # jobName=res.xpath('//div[@class="c333 font26"]/text()').extract()
        # salary=res.xpath('//span[@class="orange mr10"]/text()').extract()
        # companyName=res.xpath('//a[@class="c333 font18"]/text()').extract()
        # baseReq=res.xpath('//div[@class="font16 mt10 mb10"]//span[@class="mr10"]/text()').extract()
        # jobReq=res.xpath('//div[@class="mb20 jobdetailcon"]/text()').extract()
        # addr = res.xpath('//*[@id="jobDetail"]/div[3]/div/div/div[2]/div[3]/text()').extract()
        # info=res.xpath('//div[@class="col-xs-8"]//div//span[@class="grey"]/text()').extract()























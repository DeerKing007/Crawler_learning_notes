# -*- coding: utf-8 -*-
import random
import sys

import scrapy

from .. import items


class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com']
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
    cities = ["101010100","101020100","101280100","101280600"]
    positions = ["Python","爬虫","大数据","AI"]
    city_index = 0
    position_index = 0
    ip=["https://223.215.174.53:4286","https://117.57.37.214:4226","https://182.247.183.96:4237","https://1.70.110.197:4236","https://180.124.130.76:4243","https://220.189.86.93:2549","https://112.83.56.120:2589","https://183.188.78.75:4278","https://153.99.13.190:4276","https://114.233.165.53:4236"]
    url = "https://www.zhipin.com/c%s/?query=%s&ka=sel-city-%s"%(cities[city_index],positions[position_index],cities[city_index])

    def parse(self, response):
        req = scrapy.Request(url=self.url,callback=self.listParse,headers=self.headers,dont_filter=True)
        req.meta["proxy"] = random.choice(self.ip)
        yield req

    def listParse(self,response):
        resSel = scrapy.Selector(response)
        urls = resSel.xpath('//div[@class="info-primary"]/h3/a/@href').extract()
        for url in urls:
            req = scrapy.Request(url=self.start_urls[0]+url,callback=self.detailParse,headers=self.headers,dont_filter=True)
            req.meta["proxy"]=random.choice(self.ip)
            yield req
        nextPage = "".join(resSel.xpath('//a[@ka="page-next"]/@href').extract())
        if nextPage:
            req = scrapy.Request(url=self.start_urls[0]+nextPage,callback=self.listParse,headers=self.headers,dont_filter=True)
            req.meta["proxy"] = random.choice(self.ip)
            yield req
        else:
            if self.city_index == len(self.cities)-1: # 城市已爬取完毕
                self.city_index = 0
                if self.position_index == len(self.positions)-1: # 全部爬取完毕！
                    sys.exit()
                else:
                    self.position_index += 1
            else:
                self.city_index += 1
            req = scrapy.Request(url=self.url,headers=self.headers,dont_filter=True)
            req.meta["proxy"] = random.choice(self.ip)
            yield req

    def detailParse(self,response):
        res = scrapy.Selector(response)
        item = items.BossItem()
        item["position"] = "".join(res.xpath('//div[@class="job-primary detail-box"]//div[@class="info-primary"]//div[@class="name"]/h1/text()').extract()).replace("\n","")
        item["company"] = "".join(res.xpath('//div[@class="info"]/text()').extract()).replace(" ","").replace("\n","")
        item["salary"] = "".join(res.xpath('//div[@class="job-primary detail-box"]//div[@class="info-primary"]//div[@class="name"]/span/text()').extract()).replace(" ","").replace("\n","")
        item["requirements"] = "".join(res.xpath('//div[@class="detail-content"]//div[@class="job-sec"]/div/text()').extract()).replace(" ","").replace("\n","")
        item["experience"] = "".join(res.xpath('//div[@class="job-primary detail-box"]//div[@class="info-primary"]/p/text()').extract())
        try:
            item["education"] = res.xpath('//div[@class="job-primary detail-box"]//div[@class="info-primary"]/p/text()').extract()[2]
        except:
            item["education"]="不限"
        item["address"] = "".join(res.xpath('//div[@class="location-address"]/text()').extract()).replace(" ","")
        item["department"] = "".join(res.xpath('//a[@ka="job-detail-brandindustry"]/text()').extract())
        return item





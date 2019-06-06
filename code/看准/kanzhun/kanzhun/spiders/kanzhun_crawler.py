# -*- coding: utf-8 -*-
import scrapy
import time
from lxml import etree
# from mytools.IP代理池 import My_ip_pool
from com.fyc.kanzhun.kanzhun.items import KanzhunItem


class KanzhunCrawlerSpider(scrapy.Spider):
    name = 'kanzhun_crawler'
    allowed_domains = ['kanzhun.com']
    start_urls = ['http://kanzhun.com/']
    # my_proxies=My_ip_pool
    flag=0

    def parse(self, response):
        url="https://www.kanzhun.com/jobli_0-t_0-e_0-d_0-s_0-j_0-k_0/p/?q=%s&cityCode=%s"
        citys=[7,1,34,49]
        positions=["python web",'爬虫','大数据','AI']
        for i in citys:
            for j in positions:
                yield scrapy.Request(url=url%(j,i),callback=self.get_urls_list,dont_filter=True)


    def get_urls_list(self,response):
        res=scrapy.Selector(response).xpath('//h3[@class="r_tt"]//a/@href').extract()
        next_page=scrapy.Selector(response).xpath('//a[@class="p_next"]//@href').extract()
        for i in res:
            time.sleep(1)
            url="https://www.kanzhun.com"+i
            yield scrapy.Request(url=url, callback=self.get_detail, dont_filter=True)
        if next_page !=[]:
            url="https://www.kanzhun.com"+next_page[0]
            return scrapy.Request(url=url,callback=self.get_urls_list,dont_filter=True)

    def get_detail(self,response):
        item=KanzhunItem()
        res=scrapy.Selector(response)
        print(res.extract())
        # time.sleep(1000)
        item["company"] = res.xpath('//div[@class="company_profile"]//h1//text()').extract()
        item["position"] = res.xpath('//div[@class="company_profile"]//p//text()').extract()
        item["business"] = res.xpath('//div[@class="company_profile"]//div[@class="c_property"]//a//text()').extract()
        item["salary"] = res.xpath('//span[@class="job_salary"]//text()').extract()
        item["address"] = res.xpath('//div[@class="job"]//p[@class="info"]//a//text()').extract()
        data=res.xpath('//div[@class="job"]//p[@class="info"]//text()').extract()[0]
        data=data.split('|')
        # item["job_category"] = data[2]
        # item["education"] = data[1]
        # item["experience"] = data[0]
        # item["describe"] = res.xpath('//div[@class="job-desc_container"]//p[2]//text()').extract()
        # item["web"] = res.xpath('//div[@class="job-desc_container"]//text()').extract()[-1].split('公司网址：')[-1]
        print(item,data)
        return {}


# -*- coding: utf-8 -*-
import scrapy
from com.baizhi.Section.Section_4.utils.str_to_dict import headers_to_dict
from com.baizhi.my_demos.web_crawler.practice2.practice2.items import Practice2Item
import time


class IronSpider(scrapy.Spider):
    name = 'iron'
    allowed_domains = ['www.liepin.com']
    start_urls = ['http://www.liepin.com/']
    headers = headers_to_dict('''User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36''')

    def parse(self, response):
        cities = ['010', '020', '050020', '050090']
        kw = ['python+web', '大数据', 'AI', '爬虫']
        for i in cities:
            for j in kw:
                url = 'http://www.liepin.com/zhaopin/?dqs=%s&key=%s' % (i, j)
                yield scrapy.Request(url=url, headers=self.headers, callback=self.getUrlList)
        # 测试
        # info = {'city': '010', 'keyword': 'python+web'}
        # url = 'http://www.liepin.com/zhaopin/?dqs=%s&key=%s' % (cities[0], kw[0])
        # return scrapy.Request(url=url, headers=self.headers, callback=self.getUrlList, meta=info)

    def getUrlList(self, response):
        reqList = []
        html = scrapy.Selector(response)
        # 获取urls
        urls = html.xpath('//ul[@class="sojob-list"]//li/div/div[1]/h3/a/@href').extract()
        for url in urls:
            if 'http' in url:
                reqList.append(
                    scrapy.Request(url=url, headers=self.headers, callback=self.getJobDetail)
                )
            else:
                reqList.append(
                    scrapy.Request(url='https://www.liepin.com'+url, headers=self.headers, callback=self.getJobDetail)
                )
        # 下一页
        nextPage = ''.join(html.xpath('//a[@title="末页"]/preceding-sibling::a[1]/@href').extract())
        if 'zhaopin' in nextPage:
            reqList.append(
                scrapy.Request(url='http://www.liepin.com'+nextPage, headers=self.headers, callback=self.getUrlList)
            )
        time.sleep(2)
        return reqList

    def getJobDetail(self, response):
        item = Practice2Item()
        html = scrapy.Selector(response)
        item['jobName'] = ''.join(html.xpath('//h1/text()').extract())  # 职位名称
        item['compName'] = ''.join(html.xpath('//div[@class="title-info"]/h3/a/text()').extract())  # 公司名称
        item['salary'] = ''.join(html.xpath('//p[@class="job-item-title"]/text()').extract()).replace('\n', '').strip()  # 年薪
        # item['detailedReq'] = ''.join(html.xpath(
        #     '//div[@class="job-item main-message job-description"]/div/text() | ' +
        #     '//div[@class="job-main job-description main-message"]/div/text()'
        # ).extract()).replace('\n', '').strip()  # 任职要求
        item['experience'] = ''.join(html.xpath(
            '//div[@class="job-qualifications"]//span[2]/text() | //div[@class="resume clearfix"]//span[2]/text()'
        ).extract())  # 经验要求
        item['degree'] = ''.join(html.xpath(
            '//div[@class="job-qualifications"]//span[1]/text() | //div[@class="resume clearfix"]//span[1]/text()'
        ).extract())  # 学历要求
        item['compAddr'] = ''.join(html.xpath('//ul[@class="new-compintro"]//li[3]/text()').extract())[5:]  # 公司地址
        item['department'] = ''.join(html.xpath(
            '//div[@class="job-item main-message"]/div/ul//li[1]/label/text() | ' +
            '//div[@class="job-main main-message"][1]/div/ul//li[4]/text()'
        ).extract())  # 公司部门
        return item
        # 测试
        # print(666666666666)

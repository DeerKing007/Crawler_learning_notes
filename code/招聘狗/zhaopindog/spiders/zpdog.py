import scrapy
import json
import com.baizhi.ycx.homework.utols.解析字典 as tools
import com.baizhi.ycx.endpro.zhaopindog.zhaopindog.items as items
import time
from lxml import etree

class ZpdogSpider(scrapy.Spider):
    name = 'zpdog'
    allowed_domains = ['http://www.zhaopingou.com']
    start_urls = ['http://www.zhaopingou.com/']

    def parse(self, response):
        # 构建url
        url = 'http://qiye.zhaopingou.com/zhaopingou_interface/find_warehouse_by_position_new'
        cookies = tools.uanalysissemiColon('JSESSIONID=977D979A585AA427AFA0AF4B71B08DF8; zhaopingou_select_city=1; identity_type=1; rd_apply_lastsession_code=3; zhaopingou_login_callback=/; hrkeepToken=4A716872A790D080A9026BB16F1C2ACB; zhaopingou_account=15321015747; zhaopingou_zengsong_cookie_newDay=2019-02-19%3D3; zhaopingou_htm_cookie_newDay=2019-02-19; Hm_lvt_b025367b7ecea68f5a43655f7540e177=1550535736,1550535780,1550535845,1550555947; zhaopingou_htm_cookie_register_userName=; JSESSIONID=FC334A4E0D161895B8DE5BE05E66174D; Hm_lpvt_b025367b7ecea68f5a43655f7540e177=1550579716')
        formdata = tools.uanalysisColon('''
                                    pageSize: 0
                                    pageNo: 25 
                                    keyStrPostion: 1037
                                    postionStr: Python
                                    startDegrees: -1
                                    endDegress: -1
                                    startAge: 0
                                    endAge: 0
                                    gender: -1 
                                    timeType: -1
                                    startWorkYear: -1
                                    endWorkYear: -1
                                    isMember: -1
                                    cityId: 1
                                    isC: 0
                                    is211_985_school: 0
                                    userToken: 4A716872A790D080A9026BB16F1C2ACB
                                    clientType: 2
                                    ''')
        yield scrapy.FormRequest(url=url, callback=self.listPage, cookies=cookies, formdata=formdata, dont_filter=True)

    # 1.解析列表页 POST请求
    # 2.解析详情页 POST请求
    def listPage(self, response):
        # 初始化
        res = scrapy.Selector(response).extract().strip('<html><body><p>').strip('</p></body></html>')
        res = json.loads(res)

        url = 'http://qiye.zhaopingou.com/zhaopingou_interface/zpg_find_resume_html_details'
        for i in res['warehouseList']:
            url_ids = i['resumeHtmlId']

            formdata = tools.uanalysisColon('''
                                        resumeHtmlId: %s
                                        keyStr: 
                                        keyPositionName: 
                                        tradeId: 
                                        postionStr: 
                                        jobId: 0
                                        companyName: 
                                        schoolName: 
                                        clientNo: 
                                        userToken: 4A716872A790D080A9026BB16F1C2ACB
                                        clientType: 2
                                        '''% url_ids)
            cookies = tools.uanalysissemiColon(
                'JSESSIONID=977D979A585AA427AFA0AF4B71B08DF8; zhaopingou_select_city=1; identity_type=1; rd_apply_lastsession_code=3; zhaopingou_login_callback=/; hrkeepToken=4A716872A790D080A9026BB16F1C2ACB; zhaopingou_account=15321015747; zhaopingou_zengsong_cookie_newDay=2019-02-19%3D3; zhaopingou_htm_cookie_newDay=2019-02-19; Hm_lvt_b025367b7ecea68f5a43655f7540e177=1550535736,1550535780,1550535845,1550555947; zhaopingou_htm_cookie_register_userName=; JSESSIONID=FC334A4E0D161895B8DE5BE05E66174D; Hm_lpvt_b025367b7ecea68f5a43655f7540e177=1550579718')

            time.sleep(5)
            yield scrapy.FormRequest(url=url, callback=self.detailPage, cookies=cookies, formdata=formdata,dont_filter=True)


    # 解析详情页
    def detailPage(self, response):
        jsondata = response.text                 # 所拿到的response   （.text）获取到的为json字符串
        udic = json.loads(jsondata)              # 将字符串转化成字典
        html = etree.HTML(udic['jsonHtml'])     # 获取到jsonHtml，Element对象
        item = items.ZhaopindogItem()

        try:
            item["name"] = ''.join(html.xpath('//div[@class="resumeb-head-top"]/h2/text()'))  # 姓名
        except:
            item["name"] = ''

        item["job"] = ''.join(html.xpath('//div[@class="resumeb-head-top"]/p/text()'))  # 工作
        item["gender"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[1]/span/text()'))  # 性别
        item["age"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[2]/span/text()'))  # 年龄
        item["birthday"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[3]/span/text()'))  # 生日
        item["education"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[4]/span/text()'))  # 学历
        item["nationality"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[5]/span/text()'))  # 国籍
        item["politics_status"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[6]/span/text()'))  # 政治面貌
        item["experience"] = ''.join(html.xpath('//div[@class="resumeb-head-contact"]/p[1]/text()'))  # 工作经验
        item["address"] = ''.join(html.xpath('//div[@class="resumeb-head-contact"]/p[2]/text()'))  # 现居住地
        item["residence"] = ''.join(html.xpath('//div[@class="resumeb-head-contact"]/p[3]/text()'))  # 户籍
        item["job_nature"] = ''.join(html.xpath('//dl[@class="resume-box"]/dd/p[4]/span/text()'))  # 工作性质
        item["salayr"] = ''.join(html.xpath('//dl[@class="resume-box"]/dd/p[6]/span/text()'))  # 期望薪资

        # return item
        print(item["name"])



































































































# # -*- coding: utf-8 -*-
#
# import scrapy
# import json
# import com.baizhi.ycx.homework.utols.解析字典 as tools
# import com.baizhi.ycx.endpro.zhaopindog.zhaopindog.items as items
# import time
# from lxml import etree
#
#
# class ZpdogSpider(scrapy.Spider):
#     name = 'zpdog'
#     allowed_domains = ['http://www.zhaopingou.com']
#     start_urls = ['http://www.zhaopingou.com/']
#     upageSize = 0
#     utotal = 2000
#
#     def parse(self, response):
#         ucities = ['1','2','3','5']
#         for uct in ucities:
#             # 构建url
#             url = 'http://qiye.zhaopingou.com/zhaopingou_interface/find_warehouse_by_position_new'
#
#             if self.upageSize * 25 <= self.utotal:
#                 self.upageSize += 1
#             elif self.upageSize * 25 > self.utotal:
#                 break
#
#         cookies = tools.uanalysissemiColon('JSESSIONID=977D979A585AA427AFA0AF4B71B08DF8; zhaopingou_select_city=1; identity_type=1; rd_apply_lastsession_code=3; zhaopingou_login_callback=/; hrkeepToken=4A716872A790D080A9026BB16F1C2ACB; zhaopingou_account=15321015747; zhaopingou_zengsong_cookie_newDay=2019-02-19%3D3; zhaopingou_htm_cookie_newDay=2019-02-19; Hm_lvt_b025367b7ecea68f5a43655f7540e177=1550535736,1550535780,1550535845,1550555947; zhaopingou_htm_cookie_register_userName=; JSESSIONID=FC334A4E0D161895B8DE5BE05E66174D; Hm_lpvt_b025367b7ecea68f5a43655f7540e177=1550579716')
#         formdata = tools.uanalysisColon('''
#                                     pageSize: 0
#                                     pageNo: 25
#                                     keyStrPostion: 1037
#                                     postionStr: Python
#                                     startDegrees: -1
#                                     endDegress: -1
#                                     startAge: 0
#                                     endAge: 0
#                                     gender: -1
#                                     timeType: -1
#                                     startWorkYear: -1
#                                     endWorkYear: -1
#                                     isMember: -1
#                                     cityId: %s
#                                     isC: 0
#                                     is211_985_school: 0
#                                     userToken: 4A716872A790D080A9026BB16F1C2ACB
#                                     clientType: 2
#                                     ''' % ucities)
#
#
#         # return scrapy.FormRequest(url=url, callback=self.listPage, cookies=cookies, formdata=formdata, dont_filter=True)
#         yield scrapy.FormRequest(url=url, callback=self.listPage, cookies=cookies, formdata=formdata, dont_filter=True)
#
#     # 1.解析列表页 POST请求
#     # 2.解析详情页 POST请求
#     def listPage(self, response):
#         # 初始化
#         res = scrapy.Selector(response).extract().strip('<html><body><p>').strip('</p></body></html>')
#         # print(res)
#         res = json.loads(res)
#
#         # url_ids = []
#         url = 'http://qiye.zhaopingou.com/zhaopingou_interface/zpg_find_resume_html_details'
#         for i in res['warehouseList']:
#             # res1 = res['warehouseList']
#             # print(res1)
#             # url_id.append('http://qiye.zhaopingou.com/resume/detail?resumeId=%s' % i['resumeHtmlId'])
#
#             url_id = i['resumeHtmlId']
#             # print(url_id)
#
#             utotal = i['total']
#             print(utotal)
#
#             global utotal
#             if utotal >= 2000:
#                 self.utotal = 2000
#             else:
#                 self.upageSize = utotal // 25 + 1
#
#             formdata = tools.uanalysisColon('''
#                                         resumeHtmlId: %s
#                                         keyStr:
#                                         keyPositionName:
#                                         tradeId:
#                                         postionStr:
#                                         jobId: 0
#                                         companyName:
#                                         schoolName:
#                                         clientNo:
#                                         userToken: 4A716872A790D080A9026BB16F1C2ACB
#                                         clientType: 2
#                                         '''% url_id)
#             cookies = tools.uanalysissemiColon(
#                 'JSESSIONID=977D979A585AA427AFA0AF4B71B08DF8; zhaopingou_select_city=1; identity_type=1; rd_apply_lastsession_code=3; zhaopingou_login_callback=/; hrkeepToken=4A716872A790D080A9026BB16F1C2ACB; zhaopingou_account=15321015747; zhaopingou_zengsong_cookie_newDay=2019-02-19%3D3; zhaopingou_htm_cookie_newDay=2019-02-19; Hm_lvt_b025367b7ecea68f5a43655f7540e177=1550535736,1550535780,1550535845,1550555947; zhaopingou_htm_cookie_register_userName=; JSESSIONID=FC334A4E0D161895B8DE5BE05E66174D; Hm_lpvt_b025367b7ecea68f5a43655f7540e177=1550579718')
#
#
#             time.sleep(5)
#             # return scrapy.FormRequest(url=url, callback=self.detailPage, cookies=cookies, formdata=formdata,dont_filter=True)
#             yield scrapy.FormRequest(url=url, callback=self.detailPage, cookies=cookies, formdata=formdata,dont_filter=True)
#
#             # print(urls)
#             # return urls
#
#
#     # 解析详情页
#     def detailPage(self, response):
#         jsondata = response.text                 # 所拿到的response   （.text）获取到的为json字符串
#         udic = json.loads(jsondata)              # 将字符串转化成字典
#         html = etree.HTML(udic['jsonHtml'])     # 获取到jsonHtml，Element对象
#         item = items.ZhaopindogItem()
#
#         try:
#             item["name"] = ''.join(html.xpath('//div[@class="resumeb-head-top"]/h2/text()'))  # 姓名
#         except:
#             item["name"] = ''
#
#         item["job"] = ''.join(html.xpath('//div[@class="resumeb-head-top"]/p/text()'))  # 工作
#         item["gender"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[1]/span/text()'))  # 性别
#         item["age"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[2]/span/text()'))  # 年龄
#         item["birthday"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[3]/span/text()'))  # 生日
#         item["education"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[4]/span/text()'))  # 学历
#         item["nationality"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[5]/span/text()'))  # 国籍
#         item["politics_status"] = ''.join(html.xpath('//div[@class="resumeb-head-con"]/ul/li[6]/span/text()'))  # 政治面貌
#         item["experience"] = ''.join(html.xpath('//div[@class="resumeb-head-contact"]/p[1]/text()'))  # 工作经验
#         item["address"] = ''.join(html.xpath('//div[@class="resumeb-head-contact"]/p[2]/text()'))  # 现居住地
#         item["residence"] = ''.join(html.xpath('//div[@class="resumeb-head-contact"]/p[3]/text()'))  # 户籍
#         item["job_nature"] = ''.join(html.xpath('//dl[@class="resume-box"]/dd/p[4]/span/text()'))  # 工作性质
#         item["salayr"] = ''.join(html.xpath('//dl[@class="resume-box"]/dd/p[6]/span/text()'))  # 期望薪资
#
#         # return item
#         print(item["name"])
#
#
#
#
#
#
#
#
#
# # item["name"] = html.xpath('//div[@class="resumeb-head-top"]/h2/text()')
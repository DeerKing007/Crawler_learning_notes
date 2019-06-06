# -*- coding: utf-8 -*-
import base64
import html
import random
import re
import scrapy
import time
from fontTools.ttLib import TTFont, BytesIO
from ai145.jjw.finaljob.finaljob.items import resume58Item
from ai145.jjw.解析为字典的工具 import analysisByEqual, analysisByColon


class Resume58Spider(scrapy.Spider):
    name = 'resume58'
    allowed_domains = ['jianli.58.com']
    start_urls = ['https://j2.58cdn.com.cn/js/v8/combine/job_resume_listpage_82.js']
    headers={'user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    def parse(self, response):#入口函数
        res=scrapy.Selector(response).extract()#选择器对象
        # print(res)
        self.cities=["bj","sh","gz","sz","xa","cd","hz"]
        reobj=re.compile('listname:"(qz\w*)"')#JS中所有行业的字段正则匹配出来正则对象
        self.industry = reobj.findall(res)#所有行业的后缀
        self.cityIndex=0#城市下标
        self.industryIndex=0#行业下标
        self.pageNum=1#页码
        self.nnnn = 1
        return scrapy.Request(url='https://%s.58.com/%s/pn%s/'%(self.cities[self.cityIndex],self.industry[self.industryIndex],self.pageNum),callback=self.listParse,dont_filter=True)

    def listParse(self,response):
        res = scrapy.Selector(response)  # 选择器对象
        linkList = set(res.xpath('//div[@id="infolist"]//a/@href').extract())  # 列表页链接列表
        totalPage=int(res.xpath('//span[@class="f-red"]/text()').extract()[0])//35+1
        print(totalPage)

        for eachLink in linkList:
            if "javascript:void(0)" in eachLink:
                pass
            else:
                if "http" not in eachLink :
                    eachLink="http:"+eachLink
                time.sleep(0.8)
                print("爬详情了")
                print(eachLink)
                print("******************************************************************************")
                yield scrapy.Request(url=eachLink, callback=self.detailParse, dont_filter=True,
                                     encoding='gbk',
                                     cookies=analysisByEqual('id58=c5/nn1xpI3kzITefmb1PAg==; 58tj_uuid=d4291873-8ecb-48b8-be8d-d9814893411f; wmda_uuid=32c667dfd34ecaa883e032848d455247; wmda_visited_projects=%3B1731916484865%3B7790950805815; showPTTip=1; ljrzfc=1; als=0; wmda_session_id_1731916484865=1550397584946-a6f4bc8e-d310-29db; new_uv=2; utm_source=; spm=; init_refer=https%253A%252F%252Fpassport.58.com%252Flogout%253Fpath%253D%252F%252Fjianli.58.com%252Fresumedetail%252Fsingle%252F3_neyvnvOQnvyNTEyNTvrNlEDkTvyN_emfTvSknpsfMGOsnA5uTeyYnGUknGrsnErXlEyXnvOu%252F%2526back%253Dnow%2526PGTID%253D0d402409-0000-1152-e7d1-9408c262c032%2526ClickID%253D4; xxzl_deviceid=QJVOrQLNbks6fhHiEe1gqC2psRhyo6wtdKDZRebqO1XiCJjp%2BlHHQtBvfvyfw7%2Fo; ppStore_fingerprint=F1E8F69FFDC1294A043A04EE562A109EA6692C6FFBA9E866%EF%BC%BF1550397617427; PPU="UID=61659682689542&UN=kackacjiajia&TT=95d97c80736e39fb35c9cc39771e4879&PBODY=PuygBjoQoUvDDjcomC5872SZYzFzgJTRxV5t-ZE44Vlhi4jQ9APoIF3ypyigGmpMjuMSV4S_qPL96Zsyp8vxXJYjVQa2N-l2iQK5f5Fv_AQKsCZQRQZ81OhYdYvlJiAsOOqyZYWvjFaxOGBFxWDAToZ2buna5U5qJAoHd8Mr5og&VER=1"; www58com="UserID=61659682689542&UserName=kackacjiajia"; 58cooper="userid=61659682689542&username=kackacjiajia"; 58uname=kackacjiajia; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; new_session=0'),
                                     headers=analysisByColon('''
                                    user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36
                                     '''))

        self.pageNum+=1
        print(self.pageNum)
        time.sleep(random.randint(10,20))
        yield scrapy.Request(url='https://%s.58.com/%s/pn%s/'%(self.cities[self.cityIndex],self.industry[self.industryIndex],self.pageNum),callback=self.listParse,dont_filter=True)
        if self.pageNum>totalPage:
            time.sleep(random.randint(20,25))
            self.pageNum=1
            self.industryIndex+=1
            print(self.industryIndex)
            if self.industryIndex>=len(self.industry):
                time.sleep(random.randint(20,25))
                self.industryIndex=0
                self.cityIndex+=1
                print(self.cityIndex)
                if self.cityIndex>=len(self.cities):
                    pass

    def detailParse(self,response):
        print("111111111111111111111111111111111111")
        res = scrapy.Selector(response)  # 选择器对象
        with open('1.html','w',encoding="utf-8") as f1:
            f1.write(res.extract())
        # print(res.extract())
        try:
            name=res.xpath('//span[@id="name"]/text()').extract()[0]#名字
            print(repr(name))

            gender=res.xpath('//span[@class="sex stonefont"]/text()').extract()[0]#性别
            print(repr(gender))
            age=res.xpath('//span[@class="age stonefont"]/text()').extract()[0]#年龄
            certificate=res.xpath('//span[@class="edu stonefont"]/text()').extract()[0]#学历
            experience=res.xpath('//span[@class="stonefont"]/text()').extract()[0]#经验
            baseInfo=res.xpath('//div[@class="base-detail"]/span/text()').extract()#所有基础信息
        except:
            return None

        if len(baseInfo)==11:
            hometown=baseInfo[9]#城市
            currentLiving=baseInfo[11]#现居地
        elif len(baseInfo)==9:
            hometown=''
            currentLiving = baseInfo[9]#现居地
        else:
            hometown=''
            currentLiving = ''
        jobStatus=res.xpath('//div[@id="Job-status"]/text()').extract()[0]#求职状态
        jobExpect=res.xpath('//div[@id="expectJob"]/text()').extract()[0]#期望职位
        expectLocation=res.xpath('//div[@id="expectLocation"]/text()').extract()[0]#期望地点
        expectSalary=res.xpath('//p[@class="stonefont"]/text()').extract()[1]#期望薪资
        item=resume58Item()#类字典对象

        #-------------------------------58加密破解--------------------------------
        reobj=re.compile("base64,(.*?)\)")
        base64_str=reobj.findall(res.extract())[0]#网上woff文件路径

        def convert_font_to_xml(bin_data):#将woff转化为xml
            # 由于TTFont接收一个文件类型
            # BytesIO(bin_data) 把二进制数据当作文件来操作
            font = TTFont(BytesIO(bin_data))
            font.saveXML("text.xml")
            return None

        def comp(l1, l2):  # 定义一个比较函数，比较两个列表的坐标信息是否相同
            if len(l1) != len(l2):#坐标數是否相同
                return False
            else:
                mark = 1
                for i in range(len(l1)):
                    if abs(l1[i][0] - l2[i][0]) < 10 and abs(l1[i][1] - l2[i][1]) < 10:
                        pass
                    else:
                        mark = 0
                        break
                return mark

        # 首先进行base64解码，转化成为二进制形式，在方法中同时我也将字体文件写入了otf字体文件中
        def make_font_file(base64_string: str):
            bin_data = base64.decodebytes(base64_string.encode())
            with open('textX.woff', 'wb') as f:
                f.write(bin_data)
            return bin_data


        u_list = ['uniE0B7', 'uniE09B', 'uniE0AE', 'uniE0A1', 'uniE09A', 'uniE0B1', 'uniE0AC',
                  'uniE0B6','uniE0B3','uniE0B2','uniE0B5','uniE0A5','uniE094','uniE0A0','uniE0BD',
                    'uniE0AD','uniE098','uniE0A3','uniE0AA','uniE0A2','uniE0B4','uniE0BC','uniE0A8',
                  'uniE090','uniE09D','uniE0AB','uniE0A7','uniE0BB',
                  'uniE0B0','uniE0B9','uniE096','uniE09E','uniE097','uniE093','uniE09F','uniE092',
                  'uniE0A4','uniE0BA','uniE091','uniE0AF','uniE095','uniE09C','uniE0B8','uniE0A9','uniE0A6']#第一個

        word_list = [
            '王','8','李','女','陈','吴','7','0','士','验','应','硕','经','3','A',
            '博','届','中','9','以','大','6','赵','黄','E','张','B','专','技','1','M','周','高','4','杨','下','生','校','2',
            '5','科','无','刘','本','男'
                     ]

        #打开本地文件的库获取坐标
        def baseFont():
            font1 = TTFont('text.woff')
            be_p1 = []  # 保存（x,y）信息
            for uni in u_list:
                p1 = []  # 保存一个字符的(x,y)信息
                p = font1['glyf'][uni].coordinates  # 获取对象的x,y信息，返回的是一个GlyphCoordinates对象，可以当作列表操作，每个元素是（x,y）元组
                # p=font1['glyf'][i].flags #获取0、1值，实际用不到
                for f in p:  # 把GlyphCoordinates对象改成一个列表
                    p1.append(f)
                be_p1.append(p1)
            return be_p1

        def onlineFont():
            font2 = TTFont('textX.woff')
            uni_list2 = font2.getGlyphOrder()[1:]
            on_p1 = []
            for i in uni_list2:
                pp1 = []
                p = font2['glyf'][i].coordinates
                for f in p:
                    pp1.append(f)
                on_p1.append(pp1)
            return on_p1,uni_list2

        bin_data=make_font_file(base64_str)
        convert_font_to_xml(bin_data)
        on_p1=onlineFont()[0]
        uni_list2 = onlineFont()[1]
        be_p1=baseFont()


        n2 = 0
        x_dict = {}#临时对应字典
        for d in on_p1:
            n1 = 0
            for a in be_p1:
                if comp(a, d):
                    x_dict[uni_list2[n2][3:].lower()] = word_list[n1]
                n1 += 1
            n2 += 1
        print(x_dict)

        def replaceString(strings):#替换函数
            allcodeList=re.findall('u(\w{4})',strings)
            print(strings)
            print(allcodeList)
            for code in allcodeList:
                print(x_dict[code])
                strings=strings.replace(code,x_dict[code])
            return strings

        item['name']=replaceString(repr(name)).replace('\\u','').replace('\'','')
        item['gender']=replaceString(repr(gender)).replace('\\u','').replace('\'','')
        item['age']=replaceString(repr(age)).replace('\\u','').replace('\'','')
        item['certificate']=replaceString(repr(certificate)).replace('\\u','').replace('\'','')
        item['experience']=replaceString(repr(experience)).replace('\\u','').replace('\'','')
        item['hometown']=hometown
        item['currentLiving']=currentLiving
        item['jobStatus']=jobStatus.replace("\n",'').replace("\t",'').replace("\r",'')
        item['jobExpect']=jobExpect.replace("\n",'').replace("\t",'').replace("\r",'')
        item['expectLocation']=expectLocation.replace("\n",'').replace("\t",'').replace("\r",'')
        item['expectSalary']=replaceString(repr(expectSalary)).replace('\'','').replace("\\t",'').replace("\\n",'').replace("\\r",'').replace('\\u','')

        print(list([item['name'],item['gender'],item['age'],item['certificate'],item['experience'],item['hometown'],
                    item['currentLiving'],item['jobStatus'],item['jobExpect'],item['expectLocation'],item['expectSalary']]))

        return item

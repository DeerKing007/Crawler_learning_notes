# -*- coding: utf-8 -*-
import scrapy
import json


class MusicSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['http://music.163.com/api/v1/resource/comments/R_SO_4_415792881']
    start_urls = ['http://music.163.com/api/v1/resource/comments/R_SO_4_415792881/']

    ha = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    cook1='''_iuqxldmzr_=32; _ntes_nnid=9af168de8bff7e404194819ad1b43228,1547726202303; _ntes_nuid=9af168de8bff7e404194819ad1b43228; WM_TID=QT9XdCYrs4ZFUARVFBZ4xTbPnNuJMexj; __utma=94650624.619283242.1547726204.1547726204.1547772268.2;  __remember_me=true; P_INFO="ypb2426548694@163.com|1551661958|0|unireg|00&99|null&null&null#bej&null#10#0#0|&0||ypb2426548694@163.com"; mail_psc_fingerprint=216446eca114ed27efbee53c174b72a7; WM_NI=9ZDHrHm8DEhh%2BrLpo4AdEccbq0lBgsZiy4ONcHryO2Tt9UQ8y6zsbvWnrsAshRJChVV0GwTBUDuU%2B4GM%2F7xplaRu2VlYRMBZs%2F5haULUbZIXNj5kAD%2BjlJ7OCiZmb6niQWU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb3b169a7efb7b4b35ff4ac8ab2c45b929b9fbaf368bbbcaca9f64886be8d92e12af0fea7c3b92afb868ca9f144afe88ca6eb64e9ae8491ee4083bc8b84e26ab3f0a4a3e6799ab7b7d5ce46a198be9ace3a98acf7b6d434bbeab694e17e95b2be94c479ac8e86a4eb5e96f08998d74a979cbbb6aa408593e1d8fb7cb0bf9e96b15eb0879eaec152b1f1fb89e45f908baebbcc548eb6fb8cc450e9b6a4abb64581b7968ee13eaeb79fb8d837e2a3; playerid=71750030; MUSIC_U=8535c243b9f8cf2106f3e10ac19b251a28db88d86e5cc02701e65d42686841ecbed944fb8e36223616b54cd2fd4b43a531b299d667364ed3; __csrf=ff771ac965f0293b468163dab5b1da1c; JSESSIONID-WYYY=Ai2JyP9TnWJMaDsTkIxv22r786C1NGrwKBQ1BoNlHOhumsygNP7haqBAk0k7erh%5C9QRydccTrcoOS4OB7bhGk7OPwsF%5C9kgoVAz8%5C8Cc36n4OEKoW0fkdeE2euAKbr2TKl%2BrCDGhuSfTXvScGRkT3Bt%5CMDCIesgvxzMd0RYAttYYAVgj%3A1551884731026'''
    # 解析为字典的工具
    cookies =dict([i.strip().split('=') for i in str(cook1).split(';')])

    def parse(self, response):
        for i in range(0,10):
            url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_415792881?limit=15&offset=%s'%(i*15)
            # limit是一页的数量，offset往后的偏移。比如limit是20，offset是40，就展示第三页的
            yield scrapy.FormRequest(url=url, callback=self.commentsParse, headers=self.ha,cookies=self.cookies, dont_filter=True)

    def commentsParse(self,response):
        x = json.loads(response.body_as_unicode())
        for i in x["comments"]:
            print(i['content'])
            if i['beReplied']:
                print(i['beReplied'][0]['content'])

        '''
        https://www.zhihu.com/question/36081767  知乎(未加密接口的来源)
        
        http://www.mamicode.com/info-detail-2212136.html  对网易云音乐参数（params，encSecKey）的分析
        
        https://blog.csdn.net/qq_39268193/article/details/80171604  解析网易云的加密方式
        
        https://blog.csdn.net/lrwwll/article/details/78069013  十分钟读懂AES加密算法
        '''
        pass

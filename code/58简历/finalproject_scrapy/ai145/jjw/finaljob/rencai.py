from lxml import etree

import requests
# 用requests爬取海投网招聘信息#
# ----------------------三个工具三个类---------------------------

# 列表页工具
from ai145.jjw.finaljob.ip代理池 import IpProxiesPool
from ai145.jjw.解析为字典的工具 import analysisByEqual, analysisByColon


class listPageTool:
    # 构造方法
    def __init__(self):
        pass
    # 发送请求方法
    @staticmethod
    def sendRequest(url,requestType="get",poolObject=None,data={},params={},headers={},cookies={},proxies={},maxVolumn=10,limlit=3,**kwargs):
        # try:
        print(cookies)
        res = requests.request(url=url,method=requestType,data=data,params=params,headers=headers,cookies=cookies,**kwargs)
        print(res)
        # except:
        #     # -----若本地不行取IP代理池
        #     res = requests.request(url,requestType=requestType,data=data,params=params,headers=headers,cookies=cookies,proxies=poolObject.getOneID(),**kwargs)
        return res
    # 解析响应解析方法
    def analysisPage(self,url,**kwargs):
        res=self.sendRequest(url,**kwargs)
        print(res)
        print(res.text)
        res.encoding = res.apparent_encoding
        res=res.json()
        detailNumList=[]
        for eachE in res['data']['elements']:
            detailNumList.append(eachE['hitInfo']['jobPosting'][-10:])
        print(detailNumList)
        # linkList=eleObj.xpath('//h3[@class="job-card-search__title artdeco-entity-lockup__title ember-view"]/a/@href')
        # print(linkList)
        pass
    # 该工具接口
    def getUrl(self,url,**kwargs):
        return self.analysisPage(url=url,**kwargs)

# 详情页工具
# 入库工具


# 领英主函数
def mainFun():
    url='https://www.linkedin.com/voyager/api/search/hits?count=25&decorationId=com.linkedin.voyager.deco.jserp.WebJobSearchHit-11&distance=List()&f_C=List()&f_CF=List()&f_CT=List()&f_E=List()&f_ES=List()&f_ET=List()&f_F=List()&f_GC=List()&f_I=List()&f_JT=List()&f_L=List()&f_LF=List()&f_SB=List()&f_SB2=List()&f_SB3=List()&f_SET=List()&f_T=List()&f_TP=List()&keywords=%E7%88%AC%E8%99%AB&location=%E5%8C%97%E4%BA%AC&origin=JOB_SEARCH_RESULTS_PAGE&q=jserpAll&query=search&start=100&topNRequestedFlavors=List(HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PREFERRED_COMMUTE)'
    params=analysisByColon('''
                        count:25
                        decorationId:com.linkedin.voyager.deco.jserp.WebJobSearchHit-11
                        distance:List()
                        f_C:List()
                        f_CF:List()
                        f_CT:List()
                        f_E:List()
                        f_ES:List()
                        f_ET:List()
                        f_F:List()
                        f_GC:List()
                        f_I:List()
                        f_JT:List()
                        f_L:List()
                        f_LF:List()
                        f_SB:List()
                        f_SB2:List()
                        f_SB3:List()
                        f_SET:List()
                        f_T:List()
                        f_TP:List()
                        keywords:爬虫
                        location:北京
                        origin:JOB_SEARCH_RESULTS_PAGE
                        q:jserpAll
                        query:search
                        start:75
                        topNRequestedFlavors:List(HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PREFERRED_COMMUTE)
                        ''')
    headers=analysisByColon('''
                        accept:application/vnd.linkedin.normalized+json+2.1
                        accept-encoding:gzip, deflate, br
                        accept-language:zh-CN,zh;q=0.9
                        csrf-token:ajax:0616155508024820772
                        referer:https://www.linkedin.com/jobs/search/?keywords=%E7%88%AC%E8%99%AB&location=%E5%8C%97%E4%BA%AC&start=75
                        user-agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
                        x-li-lang:zh_CN
                        x-li-page-instance:urn:li:page:d_flagship3_search_srp_jobs;j/v1d3nSScWSaC/1IFF72w==
                        x-li-track:{"clientVersion":"1.2.7126.1","osName":"web","timezoneOffset":8,"deviceFormFactor":"DESKTOP","mpName":"voyager-web"}
                        x-restli-protocol-version:2.0.0
                        ''')
    listPageTool().getUrl(url=url,headers=headers,params=params,
                        cookies=analysisByEqual('__guid=70075158.2935097964156739600.1550569146982.7856; fid=AQGcMo_bINwjWAAAAWkFH4hWyhAzV83lF6tjc_mWW43fHO8sXi3XBaOi75VWjUfZc4pOZc-PWGCyIg; bcookie="v=2&a0876a04-6d6b-47a9-8ea0-04fc753905b5"; bscookie="v=1&20190219093906e7e43efa-4aba-4404-8cec-bc731950b146AQGNIndm6PXVmxvXzJGqaWysIkoMJEnv"; fcookie=AQFtyUIZAITTTQAAAWkFH7DzpzomWwYjEPRk5DBF8_z53cLGU4VmS0tS1XkWWToCRndPRLIEJU5Kdiamz83-cv63ZYQOdK0cT614RtgVHlbuxXtEqw5HxO9y62LI7ZXTuNyzhpH3W1GibfwTyANv_9uX22kCKYZeCnVHCWT1YWjQJsNrl8RKhcREE7webOlpnN7MdF72MPUOml4H6poKXvDrOUheUhq5iW_ooKhRb393hf_o0UhZ8ySFGqBuGAlsnHJQ9WHQzMgghi5N3CKJ6AgRoC2CmcqlBjlaY13bGnAbtLTnCL1qcw+gdvRT7He/RxM38EHIXhr2Qx+d66N4em3CGLlqy9249QX523N6diBw==; liap=true; li_at=AQEDASq-d9gE_w4vAAABaQUf-yAAAAFpKSx_IFEAXeLu_p4wazs-QQNvQmPr3Z5-Te222TVJq6IdupwYp3sA4crsfylmi6wK2VewCXttT5fLEunUsYLcSGrvG6BsAxWHuxN-maADe_sjlst7yE4aROrS; sl=v=1&e18zQ; JSESSIONID="ajax:0616155508024820772"; lang=v=2&lang=zh-cn; _lipt=CwEAAAFpBSAdvENJNR2syERuV-qxr1QVtrQr2VfCdBadCqGmT7wRDsXnFxZ8e5CwrZhkXcBpzm_lLp4uO8aa9WjBlYen8x6R-iCE5wUHfgNkfk2mC3wjaVk; _guid=eb56a767-4b03-4df4-a364-17154df4591d; li_cc=AQG7lT6jGagMsAAAAWkFIHnsbeS3ECoSBzxUBMXZ6CJW4yElqLacjb2fP_i3__Yb_JAtw9VpwcfE; UserMatchHistory=AQKcL26wpf7c1AAAAWkGDn-rf1gj_GLVziIhFVidOyio9_311Cv4n2OSXaxfcLJRVYnPJVdypsU09OxMtHA7SuSDCmVV9aEaCS3lkaGAOVSdN90U5knh0ES4gkbrRyyD01OsBw; monitor_count=40; lidc="b=SGST09:g=3:u=1:i=1550584907:t=1550650402:s=AQH3tlhCQG2r-wFd_nhvaAi-8ia4OZUG"'))



if __name__ == '__main__':
    mainFun()
import json
import re
import MySQLdb
import requests
import time
from kit工具包 import 解析字典工具 as tools
import happybase
import uuid
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
cookies=tools.analysisByEqual('JSESSIONID=A357BA64E415C64679FE364C48C3692A; Hm_lvt_b025367b7ecea68f5a43655f7540e177=1550240755,1550278719; JSESSIONID=98245623CDD86A1855E0D4419BC16966; zhaopingou_select_city=-1; rd_apply_lastsession_code=1; hrkeepToken=53D05EAA3D6D01454DCFA9BB01CFEFC7; zhaopingou_account=15210126653; zhaopingou_login_callback=/; zhaopingou_zengsong_cookie_newDay=2019-02-16%3D1; zhaopingou_htm_cookie_register_userName=; zhaopingou_htm_cookie_newDay=2019-02-16; Hm_lpvt_b025367b7ecea68f5a43655f7540e177=1550279297')
def getUrl(url,count,city):
    formdata=tools.analysisByColon('''pageSize: %s
                                        pageNo: 25
                                        keyStr: 
                                        companyName: 
                                        schoolName: 
                                        keyStrPostion: 
                                        postionStr: 
                                        startDegrees: -1
                                        endDegress: -1
                                        startAge: 0
                                        endAge: 0
                                        gender: -1
                                        region: 
                                        timeType: -1
                                        startWorkYear: -1
                                        endWorkYear: -1
                                        beginTime: 
                                        endTime: 
                                        isMember: -1
                                        hopeAdressStr: 
                                        cityId: %s
                                        updateTime: 
                                        tradeId: 
                                        startDegreesName: 
                                        endDegreesName: 
                                        tradeNameStr: 
                                        regionName: 
                                        isC: 0
                                        is211_985_school: 0
                                        clientNo: 
                                        userToken: 53D05EAA3D6D01454DCFA9BB01CFEFC7
                                        clientType: 2'''%(count,city))
    html=requests.post(url=url,headers=headers,cookies=cookies,data=formdata).text
    data=json.loads(html)

    print(data)

    detailUrls = []
    for i in data['warehouseList']:
        detailUrls.append(i['resumeHtmlId'])
    return detailUrls



def detailurl(id):

    formdata=tools.analysisByColon('''resumeHtmlId: %s
                                        keyStr: 
                                        keyPositionName: 
                                        tradeId: 
                                        postionStr: 
                                        jobId: 0
                                        companyName: 
                                        schoolName: 
                                        clientNo: 
                                        userToken: 53D05EAA3D6D01454DCFA9BB01CFEFC7
                                        clientType: 2'''%id)


    url = 'http://qiye.zhaopingou.com/zhaopingou_interface/zpg_find_resume_html_details?timestamp=%s'


    html=requests.post(url=url%str(float(time.time())*1000)[0:13],headers=headers,cookies=cookies,data=formdata).text

    data2=json.loads(html)

    try:
        return data2['shareUrl']
    except:
        return False






def resume(url):
    print('++++++++++++++++++++++++++++')
    try:
        r=re.compile('http://qiye.zhaopingou.com/share_resume\?id=(.*)')
        try:
            newid=r.findall(url)[0]

            formdata=tools.analysisByColon('htmlId:'+newid)


            newurl='http://qiye.zhaopingou.com/zhaopingou_interface/warehouse_share_info'

            html=requests.post(url=newurl,headers=headers,cookies=cookies,data=formdata).text
            time.sleep(5)

            data=json.loads(html)
            try:
                name=data['resumeHtml']['name']
            except:
                name=''
            print(name)


            try:
                age=str(data['resumeHtml']['age'])
            except:
                age=''
            #学历
            try:
                degreesName=data['resumeHtml']['degreesName']
            except:
                degreesName=''

            try:
                jobname=data['resumeHtml']['hopePosition']
            except:
                jobname=''
            #薪资
            try:
                hopeSalary=data['resumeHtml']['hopeSalary']
            except:
                hopeSalary=''
            print(hopeSalary)
            #工作经验
            try:
                jobyear=data['resumeHtml']['experience']
            except:
                jobyear=''

            try:
                #婚姻状况
                hunyin=data['resumeHtml']['hunyin']
            except:
                hunyin=''
            #户籍地
            try:
                residence=data['resumeHtml']['residence']
            except:
                residence=''
            #现居住地
            try:
                address=data['resumeHtml']['address']
            except:
                address=''



            return [name,age,degreesName,jobname,hopeSalary,jobyear,hunyin,residence,address]
        except:
            pass
    except:
        pass



conn=MySQLdb.Connect(host='localhost',
                    port=3306,
                    user='root',
                    password='123456',
                    database='spider_man',
                    charset='utf8'
                    )
cursor=conn.cursor()
# connection = happybase.Connection(host="172.16.13.200", port=9090)
#
# connection.open()



def save(param):
    sql='insert into zhaopingouee(username,age,degreesName,jobname,hopeSalary,jobyear,hunyin,residence,address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    cursor.execute(sql,param)
    conn.commit()
    # id=str(uuid.uuid4())
    # table = connection.table('zhaopingou:zhaopingouee1')
    # table.put(id,{'f1:name':param[0]})
    # table.put(id, {'f1:age': param[1]})
    # table.put(id, {'f1:degreesName': param[2]})
    # table.put(id, {'f1:jobname': param[3]})
    # table.put(id, {'f1:hopeSalary': param[4]})
    # table.put(id, {'f1:jobyear': param[5]})
    # table.put(id, {'f1:hunyin': param[6]})
    # table.put(id, {'f1:residence': param[7]})
    # table.put(id, {'f1:address': param[8]})


if __name__=="__main__":
    ct = ['1','2', '3', '5']
    url = "http://qiye.zhaopingou.com/zhaopingou_interface/find_warehouse_by_position_new"
    count=0
    for i in ct:
        while 1:

            if getUrl(url,count,i):

                for j in getUrl(url,count,i):

                    if detailurl(j):
                        save(resume(detailurl(j)))

                    else:
                        continue



                count+=1
            else:
                break
    cursor.close()
    conn.close()
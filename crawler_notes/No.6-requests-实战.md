# requests实战

* 人人网

~~~markdown
社交类网站：
1. url获取的途径：
		1. 通过推荐
		2. 通过人际关系网
		3. 通过搜索
			1. 精确
			2. 模糊
2. 数据去重：
		1. 递归的思想
		2. 数据页的数据
			1. 聚焦数据
			2. 更多的url
		3. 保证传入的url不重复
        4. 保证获取的url不重复
        	在数据库中增加了状态字段
~~~

~~~python
import requests
import 解析为字典的工具 as tools    #写好的解析工具
from lxml import etree
import MySQLdb

# 1. 登录--获取cookies ---  绑定session
# 2. 找到第一个用户  1. 手工输入姓名（昵称），状态， 主页  2. 推荐  3. 筛选（ 手工输入，固定选择）4. 最近来访，自己的好友，粉丝
# 3. 解析数据

# detailURL='http://www.renren.com/225659853/profile?v=info_timeline'
cookies=tools.analysisByEqual('anonymid=jr7j6p4slx6q4k; depovince=GW; _r01_=1; jebe_key=833708fd-59f7-4898-9db3-0c21708c1e85%7C88ebc801f31f5931b01b76a832d68a54%7C1548147765275%7C1%7C1548147583961; l4pager=0; JSESSIONID=abc2MCWXXvBeo_pupD4Hw; ick_login=bece8ea3-cb29-43dd-94ad-462c6adf0cb6; t=1d2eefc2d071cda1770306bcbf8336746; societyguester=1d2eefc2d071cda1770306bcbf8336746; id=969403126; xnsid=878abafc; ver=7.0; loginfrom=null; wp_fold=0; jebecookies=3156fae3-4954-448e-b9bd-a683004f737c|||||')
# print(requests.get(detailURL,cookies=cookies).text)
import 超级鹰.chaojiying as cjy    # 引入打码平台超级鹰
def fun2(userid,session):
    codeUrl='http://icode.renren.com/getcode.do?t=ninki&rnd=1548214464531'
    commitUrl='http://www.renren.com/validateuser.do'

    # 引入超级鹰破解
    result=cjy.Chaojiying_Client('18730231911', '999666', '898479')
    valiCode=result.PostPic(session.get(codeUrl).content,1902)['pic_str']
    postData = tools.analysisByColon('''
           id: %s
           icode: %s
           submit: 继续浏览
           requestToken: 1777621696
           _rtk: 35b5591a''' % (userid,valiCode))
    # 提交
    session.post(commitUrl,data=postData)


# 1. 访问可能认识的人的主页：主页中有多个推荐
# 2. 将多个推荐的url爬取出来
# 3. 分别访问每个个人主页的url+参数---访问资料详情页
# 4. 将数据入库
# 5. 跳转到个人主页（使用原始url）---获取访客，好友 ，粉丝的 nameCard（id）
# 6. 进一步通过namecard 访问下一层用户数据，形式：同1~5


recommendURL='http://rcd.renren.com/cwf_nget_newsfeed' # 推荐页的url
mainURL='http://www.renren.com/%s/profile'
infoURL='http://www.renren.com/%s/profile?v=info_timeline'
postData=tools.analysisByColon('''uid: 969403126
limit: 24
type: WEB_FRIEND
p: 0
requestToken: 1777621696
_rtk: 35b5591a''')
conn=MySQLdb.Connection(host='localhost',user='root',password='123456',port=3306,db='crawler',charset='utf8')
cursor=conn.cursor()
sql='insert into renren VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'


def getAndSaveUrls(i,s,mainURL):
        # 访问个人主页---进一步的拿去id
        url = mainURL % i
        # 访问并初始化
        html = etree.HTML(s.get(url).text)
        # 解析 访客id  好友id  粉丝id
        urls = html.xpath('//@namecard')[1:]
        # 去重,入库
        insert_sql='insert into renren_id VALUES (%s,0)'  # 0代表尚未被使用
        for k in urls: # k:每一个好友的id
            # 查找--unique 让数据库自己处理
            try:
                cursor.execute(insert_sql,[k])
                conn.commit()
            except Exception as e:
                pass


def analysisAndSave(s):
    select_total='select count(id) from renren_id where status=0'
    if cursor.execute(select_total)==0:  # 如果符合要求的数据为0则说已经爬取完毕
        return None

    # 从数据库中一次只拿去一个符合要求的数据
    select_sql='select id from renren_id where status=0 limit 0,1'
    result=cursor.execute(select_sql)  # result:正确执行的条数
    i=cursor.fetchone()[0]  #
    # 访问资料页---拿去自己的信息
    url2 = infoURL % i
    # 访问并初始化
    htmlInfo = etree.HTML(s.get(url2).text)
    try:
        # 解析具体信息
        temp = {}
        try:
            standardInfo = htmlInfo.xpath('//div[@class="info-section-info"]')
            schoolInfo = standardInfo[0].xpath('./dl/dd//a/text()')
            basicInfo = standardInfo[-1].xpath('.//dl[1]/dd/text() | .//dl[2]/dd/a/text() |.//dl[3]/dd/text()')
            temp['name'] = htmlInfo.xpath('//div[@class="frame-nav-inner"]/ul/li/a/text()')[0]
            temp['college'] = schoolInfo[0]
            temp['graduation'] = schoolInfo[1]
            temp['major'] = schoolInfo[2]
            #############################
            temp['gender'] = basicInfo[0]
            temp['birth'] = basicInfo[1] + '-' + basicInfo[2] + '-' + basicInfo[3]
            temp['constellation'] = basicInfo[4]
            try:
                temp['hometown'] = basicInfo[5]
            except:
                temp['hometown'] = ''
        except:
            pass
        # 数据清洗：
        for j in temp:  # i:只有键

            if not temp[j]:
                temp[j] = ''
                continue
            temp[j].strip()
            temp[j].strip(r'\n')
            temp[j].strip(r'\t')
        # 数据入库
        cursor.execute(sql, [temp['name'], temp['college'], temp['hometown'], temp['birth'], temp['gender'],
                             temp['constellation'], temp['major'], temp['graduation']])

        update_sql='update renren_id set status=1 where id=%s'
        n=cursor.execute(update_sql,[i])
        conn.commit()
    except Exception as e:
        pass

def main():
    with requests.session() as s:
        s.cookies.update(cookies)
        URLs_list = s.post(recommendURL, data=postData).json()['data']['list']
        ids = [i['id'] for i in URLs_list]
        for i in ids:
            res3 = etree.HTML(s.get(mainURL % i).text).xpath('//title/text()')[0]
            if '验证码' in res3:
                fun2(i, s)
            getAndSaveUrls(i, s, mainURL)  # 将当前页的所有好友id入库（有多个id）
            analysisAndSave(s) # 将当前页的所有数据，入库（只有当前一个id）

####################################################
if __name__ == '__main__':
    main()
~~~

![数据库去重](https://github.com/DeerKing007/Crawler_learning_notes/blob/master/crawler_notes/picture/数据库去重.png))



import requests as r
import dicttools as tools
import json

# 如果网站只能让爬取一部分信息，利用多条件，变相查询
# 如果爬取的政府网站---看的见得数据也爬取不到---无界面浏览器selenium
# 失信人：只允许爬取100条---更换GBK中的关键字，更换城市---变相的获取更多的数据 （其他的条件均只能查取100条）

# 设置文件指针的初始值
pointer=0
def getOneChinese():
    chineseword=''
    try:
        f = open('GB2312汉字.txt', 'r')
        # 先设置文件指针的位置
        global pointer
        print(pointer)
        f.seek(pointer,0)
        #
        chineseword=f.read(1)
        # 获得当前的文件指针---存到文件里/数据库
        pointer=f.tell()
    except :
        return False
    finally:
        # 关闭资源
        try:
            f.close()
        except:
            return False
    return chineseword

url='https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'
pn=0
count=0
index=0
def main():
    kw = getOneChinese()
    area = ['北京', '天津', '上海', '重庆', '河北', '山西', '陕西', '山东', '河南', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '江西', '福建',
            '湖北', '湖南', '四川', '贵州 ', '云南', '广东', '海南', '甘肃', '青海']
    headers = {
        'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E5%A4%B1%E4%BF%A1%E4%BA%BA%E6%9F%A5%E8%AF%A2&rsv_pq=d4945430000ad294&rsv_t=64a17nlLR6mtYjZ%2FcW9Rm5vU%2BaoSJJzxiglUXaZYSQnMNjxGcfkc7BTNLu0&rqlang=cn&rsv_enter=1&rsv_sug3=7&rsv_sug1=4&rsv_sug7=101',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    global count
    global pn
    global index
    data=tools.analysisByColon('''
    resource_id: 6899
    query: 失信被执行人名单
    cardNum: 
    iname: %s
    areaName: 
    ie: utf-8
    oe: utf-8
    pn: %s
    format: json
    t: 1550740352484
    cb: jQuery110206242989433968946_1550740334861
    _: 1550740334863
    '''%(kw,pn))
    res=r.get(url=url,params=data,headers=headers)
    datas=json.loads(str(res.text[46:-2]))
    print(data)
    try:
        peoples=datas['data'][0]['result']
        for i in peoples:
            # i: 每一个失信人数据
            name = i['iname']
            age = i['age']
            cardID = i['cardNum']
            caseNum = i['caseCode']
            duty = i['duty']
            date = i['regDate']
            gender = i['sexy']
            disruptypeName = i['disruptTypeName']
            performance = i['performance']
            priority = i['priority']
            type = i['type']
            update_time = i['_update_time']
            # 分页
            print(name, age, cardID, caseNum, duty, date, gender, disruptypeName, performance, priority,type, update_time)

        pn += 50
        print(pn)
        if pn>100:
            print(kw)
            kw = getOneChinese()
            pn = 0
    except:
        print(res.text)


        # 入库
if __name__ == '__main__':

    while 1:
        main()
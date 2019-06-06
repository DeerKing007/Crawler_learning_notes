import time

import requests
from lxml import etree
import MySQLdb
import json
#       1. IP数据源
# 		2. 检测可用性
# 		3. 入库存储
# 		4. 对外提供获取IP接口
# 		5. 出库
# 		6. 原则上：出库的IP应该丢弃
# 			修改状态值
# 		7. 定期检查所有入库的IP的可用性


class IpProxiesPool:
    def __init__(self,maxVolumn,limitVolumn):
        self.maxVolumn=maxVolumn #代理池容量
        self.limitVolumn=limitVolumn #阈值
        self.testUrl="http://httpbin.org/ip" #检测IP用的地址
        self.localIP = requests.get(self.testUrl).text  # 返回本地机IP，json字符串
        self.pageNum=1#初始化页数，默认均有第一页开始爬取id

    # 设置数据库初始化方法
    def initDB(self,host='localhost', port=3306, user='root', password='123456', db='crawler',charset='utf8'):
        # 设置数据库
        self.conn = MySQLdb.Connection(host=host, port=port, user=user, password=password, db=db,charset=charset)
        self.cursor = self.conn.cursor()
        self.insertSQL = 'insert into proxies(proxy,status) values(%s,%s)'
        self.countSQL = 'select status from proxies where status=0'
        self.selectSQL = 'select proxy from proxies where status=0 limit 0,1'
        self.updateSQL = 'update proxies set status=1 where proxy=%s'


    #1. 获取IP来源
    def provideIP(self,url="https://www.kuaidaili.com/free/inha/"):
        header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        while self.getCount()<self.maxVolumn:
            eleObj=etree.HTML(requests.get(url+str(self.pageNum),headers=header).text)#向代理网站发送请求
            for eachRow in eleObj.xpath("//tbody/tr"):
                self.IPnum,self.port,self.protocol=eachRow.xpath("./td[1]/text() | ./td[2]/text() | ./td[4]/text()")
                proxy={self.protocol:self.IPnum+":"+self.port}#构成代理参数
                print(proxy)
                # 传给检测IP是否有效
                if self.validateIP(proxy):
                    # 可用 入库
                    print('yassssssssssssssssssssssssssssssssssssssss')
                    try:#尝试是否在库里重复

                        self.saveOneIP(proxy)
                    except:
                        pass

            if self.pageNum>1000:
                self.pageNum=0
            self.pageNum+=1
            time.sleep(10)
            self.regularValidate()#----此页获取完后，常规检测全表IP有没有过期！！
    #2. 获取一个IP
    def getOneID(self):
        # 选查询的第一个
        self.cursor.execute(self.selectSQL)
        proxy = json.loads(self.cursor.fetchone()[0])
        # 标记已用IP
        self.cursor.execute(self.updateSQL, [proxy])
        self.conn.commit()
        self.autoAddIP()
        return proxy

    #辅助：自动补货方法
    def autoAddIP(self):
        # 刷新一次数据库
        self.regularValidate()
        # 判断是否达到阈值
        if self.getCount() <= self.limit:
            # 加满
            self.provideIP()


    # 辅助：常规检测表里的所有IP，
    def regularValidate(self):
        for i in self.getAllIPs():
            if self.validateIP(i):
                # 可用！初始化状态0
                self.cursor.execute('update proxies set status=0 where proxy='+str(i))
                self.conn.commit()
            else:
                # 不可用！更变为已用状态
                self.cursor.execute('update proxies set status=1 where proxy=' + str(i))
                self.conn.commit()

    # 辅助：获取数据库里所有代理
    def getAllIPs(self):
        self.cursor.execute('select proxy from proxies')
        for j in [i[0] for i in self.cursor.fetchall()]:
            # j: 每一个proxy
            yield json.loads(j)#生成器对象

    # 辅助： 将可用的IP入库
    def saveOneIP(self, proxy):
        self.cursor.execute(self.insertSQL, [str(proxy), 0])  # 0:可用
        self.conn.commit()

    # 辅助：检测IP可用性
    def validateIP(self,proxy):
        if self.localIP==requests.get(self.testUrl,proxies=proxy).text:# IP无效失败--丢弃
            return False
        return True

    # 辅助：在数据库查看有效IP总条数
    def getCount(self):
        return self.cursor.execute(self.countSQL)

if __name__ == '__main__':
    a=IpProxiesPool(10,3)# 最大值为10，阈值为3
    a.initDB(db="crawer")
    a.provideIP()  # 1. 自动补满了IP  2. 如果小于阈值，自动补冲 3. 根据情况自动刷新数据库，筛选出可用IP（包括新的和旧的）

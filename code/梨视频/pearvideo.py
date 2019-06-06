import requests
from lxml import etree
import re
import os
import urllib.request


def download():
    # 获取网页源代码
    url = "http://www.pearvideo.com/category_8"
    # 模拟浏览器去请求服务器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    }

    req = requests.get(url=url, headers=headers).text

    html = etree.HTML(req)
    # 获取视频id
    video_id = html.xpath('//a[@class="vervideo-lilink actplay"]/@href')

    # 拼接URL地址
    video_url = []  # 接收拼接好的url
    starturl = 'http://www.pearvideo.com' + ''
    for vid in video_id:
        newurl = starturl + '/' + vid
        video_url.append(newurl)

    # 获取视频播放地址
    for purl in video_url:
        req = requests.get(purl, headers=headers)
        reg = 'ldUrl="",srcUrl="(.*?)"'
        playurl = re.findall(reg, req.text)
        html = etree.HTML(req.text)
        video_name = html.xpath('//h1[@class="video-tt"]/text()')

        print('正在下载视频%s' % video_name)

        path = 'video'
        if path not in os.listdir():
            os.mkdir(path)

        filepath = path + "/%s" % video_name[0].replace(':', '') + '.mp4'
        print(filepath)


        # 下载
        try:
            print(playurl[0])
            urllib.request.urlretrieve(playurl[0], filepath)
            print('%s下载成功' % video_name)
        except:
            print('%s下载失败' % video_name)

download()
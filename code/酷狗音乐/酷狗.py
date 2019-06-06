import requests
from lxml import etree
import json
import demjson
import re
url = "https://songsearch.kugou.com/song_search_v2?callback=jQuery11240703352865556796_1548925855657&keyword=%E6%9C%80%E9%95%BF%E7%9A%84%E7%94%B5%E5%BD%B1&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1548925855659"
res=requests.get(url).text
data=re.compile('"FileName":"(.*?)-')
name1=data.findall(res)[0]
data1=re.compile('"FileName":"周杰伦(.*?)","AlbumID":')
name2=data1.findall(res)[0].replace("<em>","").replace("<\/em>","")
name=name1+name2
print(name)
file_hush=re.findall('"FileHash":"(.*?)"',res)[0]
print(file_hush)
hush_url='https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19108062041247404896_1548940404937&hash='+file_hush
hush_html=requests.get(hush_url).text
url_data=re.compile('"play_url":"(.*?)","authors":')
hurl=url_data.findall(hush_html)[0].replace("\\","")
print(hurl)
with open(name+'.mp3','wb') as f:
    f.write(requests.get(hurl).content)
print("下载完毕")

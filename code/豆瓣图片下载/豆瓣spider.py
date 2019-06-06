import scrapy
import json
from ..items import Douban
class DouBanSpider(scrapy.Spider):
    name = "douban"

    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.181 Safari/537.36"}


    def start_requests(self):
        movie_api = 'https://movie.douban.com/j/search_subjects?' \
                    'type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend' \
                    '&page_limit=100&page_start=0'
        yield scrapy.Request(url=movie_api,headers=self.headers,callback=self.parse)
    def parse(self, response):
        item = Douban()
        res = json.loads(response.text)
        # l = []
        for i in res["subjects"]:
            # l.append(i["cover"])
            item["image_urls"] = [i["cover"]]
            item["image_store"] = i["title"]
            yield item




# -*- coding: utf-8 -*-

# Scrapy settings for finaljob project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'finaljob'

SPIDER_MODULES = ['finaljob.spiders']
NEWSPIDER_MODULE = 'finaljob.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'finaljob (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
    ':authority':'jianli.58.com',
    ':method':'GET',
':path':'/resumedetail/singles/3_neyvnvOQnvyNTEyNTvrNlEDkTvyN_emfTvSknpsfMGOsnA5uTeyYnGUknGrsnErXlEyXnvOu?psid=193585330203212951230839606&entinfo=3_neyvnvOQnvyNTEyNTvrNlEDkTvyN_emfTvSknpsfMGOsnA5uTeyYnGUknGrsnErXlEyXnvOu_z&sourcepath=pc-jllista-zhineng&f=pc_list_detai&dpid=4ba1576d5b99494e8fdf935c2fb351c6&followparam=%7B%22searchID%22%3A%221ed1ff5d9c8a45ad9e3959aa343b1f5c%22%2C%22searchVersion%22%3A10000%2C%22searchAreaID%22%3A1%2C%22searchFirstAreaID%22%3A1%2C%22searchPositionID%22%3A2076%2C%22searchSecondPositionID%22%3A2076%2C%22page%22%3A1%2C%22location%22%3A9%2C%22resumeType%22%3A2%2C%22platform%22%3A%22pc%22%2C%22sourcePage%22%3A%22pc-jllista-zhineng%22%2C%22operatePage%22%3A%22list%22%7D&adtype=3',
':scheme':'https',
'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding':'gzip, deflate, br',
'accept-language':'zh-CN,zh;q=0.9',
'cache-control':'max-age=0',
'cookie':'id58=c5/nn1xozWcxuePjlDzCAg==; 58tj_uuid=42dd32b7-f629-4f4a-8527-af08659346a2; xxzl_deviceid=KIZUqHwRnIz9xd7dQ7AwxTOvAoE1kqxdX1GEx212%2BVZYl71bnJPRvHueToGRL4qN; als=0; __guid=11522095.181827195578354240.1550372605707.7844; showPTTip=1; ljrzfc=1; wmda_uuid=e0665e2b4d67afbd402d1382fa012dd5; wmda_new_uuid=1; wmda_visited_projects=%3B1731916484865; guide=1; param8616=0; param8716kop=1; jl_list_left_banner=101; new_uv=3; utm_source=; spm=; init_refer=; new_session=0; wmda_session_id_1731916484865=1550383843317-33e70163-df4e-ed3f; 58home=bj; city=bj; xxzl_smartid=f0e11c0d2e861afca7f6bce729df8794; showOrder=1; Hm_lvt_a3013634de7e7a5d307653e15a0584cf=1550391260; Hm_lpvt_a3013634de7e7a5d307653e15a0584cf=1550391260; show_zcm_banner=true; sessionid=53a8a788-9f47-47bd-8030-2429574f965a; www58com="UserID=61659682689542&UserName=kackacjiajia"; 58cooper="userid=61659682689542&username=kackacjiajia"; 58uname=kackacjiajia; PPU="UID=61659682689542&UN=kackacjiajia&TT=8b825b0521647021d3e5d51a08bd6046&PBODY=PxovX7S2JdCS0LU4WIKWFkKjN5DE6bLBBHGzebFtg1atniW_yW6GiJbXpTSh6Qo7dAtS-TWxF4jVKaDWn-m358FoHSs4C-i5C98vpdiByasr2_zZPXHW_JNuFFy3kEyYwSElGO_7BCpy2S-cN3i25Opi0ZQU8e0-mItTowOM4N8&VER=1"; ppStore_fingerprint=045EE9109B21D2DE0F9EEEE90B86D347D70BB9D6A10DBD65%EF%BC%BF1550392305811; monitor_count=63',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'finaljob.middlewares.FinaljobSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'finaljob.middlewares.FinaljobDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'finaljob.pipelines.JobPipeline': 300,
   'finaljob.pipelines.resume58Item': 302,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
#FEED_EXPORT_ENCODING = 'utf-8'
# MyHost="192.168.0.201"
# Port=9090
# LOG_FILE="mySpider.log"
# LOG_LEVEL="INFO"
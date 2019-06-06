# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Practice2Item(scrapy.Item):
    jobName = scrapy.Field()
    compName = scrapy.Field()
    salary = scrapy.Field()
    # detailedReq = scrapy.Field()
    experience = scrapy.Field()
    degree = scrapy.Field()
    compAddr = scrapy.Field()
    department = scrapy.Field()

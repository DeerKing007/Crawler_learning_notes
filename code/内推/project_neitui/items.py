# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectNeituiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobName = scrapy.Field()
    salary = scrapy.Field()
    companyName = scrapy.Field()
    baseReq = scrapy.Field()
    jobReq = scrapy.Field()
    addr = scrapy.Field()
    info = scrapy.Field()

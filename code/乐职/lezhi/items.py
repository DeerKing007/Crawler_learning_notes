# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LezhiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    jobname=scrapy.Field()
    education=scrapy.Field()
    age=scrapy.Field()
    hope_place=scrapy.Field()
    hope_salary=scrapy.Field()
    work_experience=scrapy.Field()
    sex=scrapy.Field()
    now_status=scrapy.Field()
    person_information=scrapy.Field()

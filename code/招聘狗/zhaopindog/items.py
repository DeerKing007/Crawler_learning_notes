# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopindogItem(scrapy.Item):
    name = scrapy.Field()
    job = scrapy.Field()
    gender = scrapy.Field()
    age = scrapy.Field()
    birthday = scrapy.Field()
    education = scrapy.Field()
    nationality = scrapy.Field()
    politics_status = scrapy.Field()
    experience = scrapy.Field()
    address = scrapy.Field()
    residence = scrapy.Field()
    job_nature = scrapy.Field()
    salayr = scrapy.Field()
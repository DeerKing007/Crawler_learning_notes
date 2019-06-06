# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    positionName=scrapy.Field()
    pproperty=scrapy.Field()
    salary=scrapy.Field()
    city=scrapy.Field()
    quantity=scrapy.Field()
    experience=scrapy.Field()
    certificate=scrapy.Field()
    companyName=scrapy.Field()
    scale=scrapy.Field()
    industry=scrapy.Field()
    comCharacter=scrapy.Field()
    officialLink=scrapy.Field()
    comDesc=scrapy.Field()
    location=scrapy.Field()

class resume58Item(scrapy.Item):
    name = scrapy.Field()
    gender = scrapy.Field()
    age = scrapy.Field()
    certificate = scrapy.Field()
    experience = scrapy.Field()
    hometown = scrapy.Field()
    currentLiving = scrapy.Field()
    jobStatus = scrapy.Field()
    jobExpect = scrapy.Field()
    expectLocation = scrapy.Field()
    expectSalary = scrapy.Field()


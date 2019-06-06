# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QianchengwuyouItem(scrapy.Item):
    # define the fields for your item here like:
    job_name=scrapy.Field()
    job_salary=scrapy.Field()
    company_name=scrapy.Field()
    job_info=scrapy.Field()
    job_experience=scrapy.Field()
    job_stady=scrapy.Field()
    job_addr=scrapy.Field()
    company_info=scrapy.Field()
    company_nature=scrapy.Field()
    company_scale=scrapy.Field()
    company=scrapy.Field()
    job=scrapy.Field()
    addr=scrapy.Field()
    person=scrapy.Field()
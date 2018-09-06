# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    job = scrapy.Field()
    uptime = scrapy.Field()
    exper = scrapy.Field()
    edu = scrapy.Field()
    loc = scrapy.Field()
    brief_company = scrapy.Field()
    host = scrapy.Field()

class IvestItem(scrapy.Item):
    website = scrapy.Field()
    company = scrapy.Field()
    industry = scrapy.Field()
    city = scrapy.Field()
    round = scrapy.Field()
    number = scrapy.Field()
    angle = scrapy.Field()
    time = scrapy.Field()

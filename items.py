# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GlassdoorItem(scrapy.Item):
    title = scrapy.Field()
    empname = scrapy.Field()
    location = scrapy.Field()
    size = scrapy.Field()
    salarylow = scrapy.Field()
    salaryhigh = scrapy.Field()
    jobId = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
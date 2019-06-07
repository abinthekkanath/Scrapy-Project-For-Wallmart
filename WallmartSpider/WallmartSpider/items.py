# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WallmartspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    currentPrice=scrapy.Field()
    oldPrice=scrapy.Field()
    userRating=scrapy.Field()
    aboutItem=scrapy.Field()
    specifications=scrapy.Field()

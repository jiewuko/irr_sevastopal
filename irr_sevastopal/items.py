# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IrrSevastopalItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    type_ = scrapy.Field()
    owner_name = scrapy.Field()
    address = scrapy.Field()
    published_date = scrapy.Field()
    price = scrapy.Field()
    telephone = scrapy.Field()
    agency = scrapy.Field()


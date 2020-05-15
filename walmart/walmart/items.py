# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WalmartItem(scrapy.Item):
    # define the fields for your item here like:
    #Product
    store = scrapy.Field()
    sku = scrapy.Field()
    upc = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    imageUrl = scrapy.Field()
    url1 = scrapy.Field()
    brand = scrapy.Field()
    package = scrapy.Field()

    #branchProducts
    productId = scrapy.Field()
    branch = scrapy.Field()
    stock = scrapy.Field() #falta
    price = scrapy.Field()

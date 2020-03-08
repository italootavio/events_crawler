# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Event(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    info_city = scrapy.Field()
    info_calendar = scrapy.Field()
    description = scrapy.Field()
    ticket_types = scrapy.Field()
    ticket_values = scrapy.Field()
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SarjisItem(scrapy.Item):
    name = scrapy.Field()
    date_crawl = scrapy.Field()
    date_publish = scrapy.Field()
    number = scrapy.Field()
    title = scrapy.Field()
    alt = scrapy.Field()
    img_url = scrapy.Field()
    pass

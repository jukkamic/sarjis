# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# name, date, number, title, alt, img_url

class SarjisItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    number = scrapy.Field()
    title = scrapy.Field()
    alt = scrapy.Field()
    imgurl = scrapy.Field()
    pass

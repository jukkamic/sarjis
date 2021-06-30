import scrapy


class XkcdSpider(scrapy.Spider):
    name = 'xkcd'
 #   allowed_domains = ['xkcd.com']
 #   start_urls = ['http://xkcd.com/']
#    allowed_domains = ['*']
    start_urls = ["http://54.217.147.107/xkcd/"]

    def parse(self, response):
        for comic in response.xpath('//div[@id="middleContainer"]'):
            #            comic = response.xpath('//div[@id="middleContainer"]')

            #            print("COMIC === " + comic)
            title = comic.xpath('//div[@id="ctitle"]/text()').extract_first()
            imgurl = "https:" + comic.xpath('//div[@id="comic"]/img/@src').extract_first()
            alt = comic.xpath('//div[@id="comic"]/img/@title').extract_first()
            yield {
                'name': "xkcd",
                'title': title,
                'imgurl': imgurl,
                'alt': alt,
            }


#            yield {
#                'title': title,
#                'imgurl': strip.xpath('.´/div[@id="comic"]/img/@src').extract_first(),
#                'alt': strip.xpath('./div[@id="comic"]/img/@title').extract_first(),
#            }

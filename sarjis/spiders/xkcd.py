import scrapy

class XkcdSpider(scrapy.Spider):
    name = 'xkcd'
#    allowed_domains = ['xkcd.com']
#    start_urls = ['http://xkcd.com/']
    start_urls = ["http://54.217.147.107/xkcd/"]

    count:int = 1

    def parse(self, response):
        for comic in response.xpath('//div[@id="middleContainer"]'):
            title = comic.xpath('//div[@id="ctitle"]/text()').extract_first()
            imgurl = "https:" + comic.xpath('//div[@id="comic"]/img/@src').extract_first()
            alt = comic.xpath('//div[@id="comic"]/img/@title').extract_first()
            yield {
                'name': "xkcd",
                'title': title,
                'imgurl': imgurl,
                'alt': alt,
            }
        next_page = response.xpath('//a[@rel="prev"]/@href').extract_first()
        if next_page is not None and self.count < 5:
            self.count = self.count + 1
            # remove count limit
            print("count: ", self.count)
#            yield scrapy.Request(response.urljoin(next_page))
            yield scrapy.Request(response.urljoin("/xkcd" + next_page))



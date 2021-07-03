import scrapy

class XkcdSpider(scrapy.Spider):
    name = 'xkcd'
#    allowed_domains = ['xkcd.com']
    start_urls = ['http://xkcd.com/']
#    start_urls = ["http://54.217.147.107/xkcd/"]

    count:int = 1

    def parse(self, response):
        for comic in response.xpath('//div[@id="middleContainer"]'):
            title = comic.xpath('//div[@id="ctitle"]/text()').extract_first()
            img_url = "https:" + comic.xpath('//div[@id="comic"]/img/@src').extract_first()
            alt = comic.xpath('//div[@id="comic"]/img/@title').extract_first()
            yield {
                'id': 0,
                'name': self.name,
                'date_crawl': '1999-01-01',
                'date_publish':'1999-01-01',
                'number': '0',
                'title': title,
                'img_url': img_url,
                'alt': alt,
            }
        next_page = response.xpath('//a[@rel="prev"]/@href').extract_first()
        if next_page is not None and self.count < 5:
            self.count = self.count + 1
            # remove count limit
            print("count: ", self.count)
            print("next_page: ", next_page)
            print("with urljoin: ", response.urljoin(next_page))
            yield scrapy.Request(response.urljoin(next_page))
#            yield scrapy.Request(response.urljoin("/xkcd" + next_page))



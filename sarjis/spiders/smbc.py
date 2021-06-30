import scrapy

class SmbcSpider(scrapy.Spider):
    name = 'smbc'
    start_urls = ['https://www.smbc-comics.com/']

    count:int = 1

    def parse(self, response):
        for comic in response.xpath('//div[@id="mainwrap"]'):
            alt = comic.xpath('//img[@id="cc-comic"]/@title').extract_first()
            imgurl = "https:" + comic.xpath('//img[@id="cc-comic"]/@src').extract_first()
            yield {
                'name': self.name,
                'title': '',
                'date': '',
                'number': '',
                'imgurl': imgurl,
                'alt': alt,
            }
        next_page = response.xpath('//a[@class="cc-prev"]/@href').extract_first()
        if next_page is not None and self.count < 5:
            self.count = self.count + 1
            # remove count limit
            print("count: ", self.count)
            yield scrapy.Request(response.urljoin(next_page))



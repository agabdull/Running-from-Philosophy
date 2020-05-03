import scrapy
seen_pages = []

class QuotesSpider(scrapy.Spider):
    name = "wiki_spider"
    start_urls = [
        'https://en.wikipedia.org/wiki/Hank_Green'
    ]

    def parse(self, response):
        with open('list_of_pages.txt', 'a') as f:
            f.write((response.css('title::text').get())[:-12]+"\n")
            f.close()
            
        next_page = response.css('#mw-content-text > div > p > a::attr(href)').get()

        if (next_page != None) and (not(next_page in seen_pages)):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        

import scrapy
from scrapy.crawler import CrawlerProcess
import re
import clean

pattern = re.compile("\/wiki\/(\w|\(|\)|-)*")

class WikiSpider(scrapy.Spider):
    name = "wiki"
    start_urls = ['https://en.wikipedia.org/wiki/Bielefeld']

    def parse(self, response):
        title = ""
        with open('list_of_pages.txt', 'a') as f:
            title = (response.css('title::text').get())[:-12]+"\n"
            f.write(title)
            f.close()

        potential_match = ""
        next_page = ""
        para_arr = response.css('#mw-content-text > div > p').getall() #array of strings of paragraphs
        for para in para_arr:
            while (pattern.search(para)):
                potential_match = pattern.search(para)  # get first prospective url
                my_index = potential_match.span()[0]
                came_before = para[:my_index]
                if clean.balanced_parens(came_before):
                    next_page = potential_match.group(0)
                    break
                else:
                    #removing first slash of the link so that it no longer matches,
                    # and continue searching for hyperlinked articles in the current paragraph
                    para = para[:my_index]+"CHECKED"+para[my_index+1:]

            if next_page != "":
                break


        if ((next_page != "") and (title != "Philosophy\n")):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


process = CrawlerProcess()
process.crawl(WikiSpider)
process.start() # the script will block here until the crawling is finished

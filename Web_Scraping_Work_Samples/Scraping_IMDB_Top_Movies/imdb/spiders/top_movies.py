# -*- coding: utf-8 -*-
import scrapy


class TopMoviesSpider(scrapy.Spider):
    name = 'top_movies'
    allowed_domains = ['www.imdb.com/']
    # start_urls = ['https://www.imdb.com/search/title/?genres=action,drama/']

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=action,drama/', callback=self.parse,headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
        })

    def parse(self, response):
        for movie in response.xpath("//div[@class='lister-list']/div"):
            yield{
                'movie_name':movie.xpath(".//h3/a/text()").get(),
                'year':movie.xpath(".//h3/span[@class='lister-item-year text-muted unbold']/text()").get(),
                'imdb_rating':movie.xpath(".//div[@class='inline-block ratings-imdb-rating']/strong/text()").get(),
                'votes':movie.xpath(".//p[@class='sort-num_votes-visible']/span[2]/text()").get()
            }

        next_page=response.xpath("(//a[@class='lister-page-next next-page'][1]/@href)[2]").get()
        print(next_page)

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse,headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
        })

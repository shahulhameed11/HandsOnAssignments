# -*- coding: utf-8 -*-
import scrapy


class TopMoviesSpider(scrapy.Spider):
    name = 'top_movies'
    allowed_domains = ['www.imdb.com/']
    start_urls = ['https://www.imdb.com/chart/top/']

    def parse(self, response):
        for movie in response.xpath("//tbody[@class='lister-list']/tr"):            
            yield {
                'title':movie.xpath(".//td[@class='titleColumn']/a/text()").get(),
                'year':movie.xpath(".//td[@class='titleColumn']/span/text()").get(),
                'imdb_rating':movie.xpath(".//td[@class='ratingColumn imdbRating']/strong/text()").get()
            }

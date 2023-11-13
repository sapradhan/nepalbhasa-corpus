# -*- coding: utf-8 -*-
import scrapy


class NepalMandalSpider(scrapy.Spider):
    name = 'nepalmandal'
    allowed_domains = ['www.nepalmandal.com']

    def start_requests(self):
        urls = ['https://www.nepalmandal.com/cat/31/1.html',
                'https://www.nepalmandal.com/blog/1.html']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        blog_container = response.css('div#content p.content::text')

        if blog_container:
            yield { 'url': response.url,
                   'header': response.css("h1.title::text").get() or "", 
               'date' : response.css("div#content > div.post > div.byline small::text").get()[10:],
               'text': '\n'.join ([response.css("div#content > div.post > h1::text").get().strip()] + [line.strip() for line in blog_container.getall() if line.strip()]) }
        else: 
            for link in response.css('div#content a.nepali::attr(href)'):
                yield response.follow(link, callback = self.parse)

            next_page = response.xpath("//div[@id='content']/div[@class='post']/div[1]/a[text()=' next ']/@href").get()
            if next_page is not None:
                yield response.follow(next_page, callback = self.parse)

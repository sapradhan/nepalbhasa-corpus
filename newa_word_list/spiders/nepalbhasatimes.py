# -*- coding: utf-8 -*-
import scrapy


class NepalbhasatimesTextSpider(scrapy.Spider):
    name = 'nepalbhasatimes'
    allowed_domains = ['nepalbhasatimes.com']
    
    def start_requests(self):
        urls = ['https://nepalbhasatimes.com/category/%e0%a4%ac%e0%a5%81%e0%a4%96%e0%a4%81',
            'https://nepalbhasatimes.com/category/%e0%a4%ac%e0%a4%bf%e0%a4%9a%e0%a4%be%e0%a4%83',
            'https://nepalbhasatimes.com/category/%e0%a4%a8%e0%a5%87%e0%a4%b5%e0%a4%be%e0%a4%83%e0%a4%96%e0%a5%8d%e0%a4%af%e0%a4%83',
            'https://nepalbhasatimes.com/category/%e0%a4%b8%e0%a4%82%e0%a4%b8%e0%a5%8d%e0%a4%95%e0%a5%83%e0%a4%a4%e0%a4%bf',
            'https://nepalbhasatimes.com/category/%e0%a4%b8%e0%a4%be%e0%a4%b9%e0%a4%bf%e0%a4%a4%e0%a5%8d%e0%a4%af',
            'https://nepalbhasatimes.com/category/%e0%a4%85%e0%a4%b0%e0%a5%8d%e0%a4%a5',
            'https://nepalbhasatimes.com/category/%e0%a4%95%e0%a4%be%e0%a4%b8%e0%a4%be%e0%a4%96%e0%a5%8d%e0%a4%af',
            'https://nepalbhasatimes.com/category/%e0%a4%a8%e0%a5%8d%e0%a4%b9%e0%a5%8d%e0%a4%af%e0%a4%87%e0%a4%aa%e0%a5%81%e0%a4%96%e0%a5%8d%e0%a4%af%e0%a4%83',
            'https://nepalbhasatimes.com/category/%e0%a4%b6%e0%a5%81%e0%a4%95%e0%a5%8d%e0%a4%b0%e0%a4%b5%e0%a4%be%e0%a4%83%e0%a4%af%e0%a4%be-%e0%a4%a4%e0%a4%81%e0%a4%b8%e0%a4%be%e0%a4%aa%e0%a5%8c'
            ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        blog_container = response.css('.blog-single-details')

        if blog_container:
            yield { 'url': response.url,
               'header': response.css('h1::text').get() or " ",
               'date' : response.css('.post-single-info > ul > li:nth-child(2) > a::text').get() or " ",
               'text': '\n'.join ([line.strip() for line in  response.css('.blog-single-details > p::text').getall()]) }
        else: 
            for link in response.css('div.post-style4[itemtype="http://schema.org/BlogPosting"] h3 a[itemprop="url"]'):
                yield response.follow(link, callback = self.parse)

            next_page = response.css('a.next.page-numbers::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, callback = self.parse)

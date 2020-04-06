# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["sirena.do"]
    start_urls = [
        'http://sirena.do/products/category/abarrotes/',
    ]

    def parse(self, response):
        for product_url in response.css("div.item-card > a.item-title ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(product_url), callback=self.parse_product_page)
        next_page = response.css("ul.pagination > li:last-of-type > a.page-link ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_product_page(self, response):
        item = {}
        
        product = response.css("div.item-info")
        cat = response.css("div.path-title")

        item["title"] = product.css("h1 ::text").extract_first()
        item['parent'] = cat.css("a:first-of-type ::text").extract_first()
        item['category'] = cat.css("a:last-of-type ::text").extract_first()
        item['image'] = product.css(".large-pic > div ::attr(style)").re_first('background-image: (.*)$')
        item['description'] = product.css("div.has-inform ::text").extract_first()
        item['price'] = product.css("h2 ::text").extract_first()
        yield item
        

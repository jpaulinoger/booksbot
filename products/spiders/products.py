# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["sirena.do"]
    start_urls = [
        'https://sirena.do/products/category/desechables',
        'https://sirena.do/products/category/frutas-y-vegetales',
        'https://sirena.do/products/category/graneria',
        'https://sirena.do/products/category/lacteos-y-huevos',
        'https://sirena.do/products/category/limpieza-del-hogar',
        'https://sirena.do/products/category/panaderia-y-reposteria',
        'https://sirena.do/products/category/pescados-y-mariscos-',
        'https://sirena.do/products/category/picaderas-dulces',
        'https://sirena.do/products/category/picaderas-saladas',
        'https://sirena.do/products/category/miscelaneos',
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
        item['description'] = product.css("div.has-inform > p ::text").extract_first()
        item['description2'] = product.css("div.has-inform ::text").extract()
        item['price'] = product.css("h2 ::text").extract_first()
        yield item
        

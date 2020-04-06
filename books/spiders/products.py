# -*- coding: utf-8 -*-
import scrapy


class productsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["books.toscrape.com"]
    start_urls = [
        'http://books.toscrape.com/',
    ]

    def parse(self, response):
        for product_url in response.css("article.book_pod > h3 > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(product_url), callback=self.parse_product_page)
        next_page = response.css("li.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_product_page(self, response):
        item = {}
        product = response.css("div.book_main")
        item["title"] = product.css("h1 ::text").extract_first()
        item['category'] = response.xpath(
            "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()"
        ).extract_first()
        item['description'] = response.xpath(
            "//div[@id='book_description']/following-sibling::p/text()"
        ).extract_first()
        item['price'] = response.css('p.price_color ::text').extract_first()
        yield item

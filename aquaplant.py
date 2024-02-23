import scrapy
import pandas as pd

class Aquaplant(scrapy.Spider):
    name = 'aquaplant'

    def start_requests(self):
        urls = ['https://shop.aquaplantstudio.com/products/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = []
        product_divs = response.css('.product-wrapper')
        for product_div in product_divs:
            href = product_div.css('h3 a::attr(href)').get()
            links.append(href)
        for link in links:
            yield response.follow(link, callback=self.get_data)

    def get_data(self, response):
        product_name = response.css('.summary-inner set-mb-l reset-last-child h1::text').get()
        product_price = response.css('.price span bdi::text').get()
        product_sku = response.css('.product_meta span::text').get()[2]
        product_description = response.css('.wd-accordion-item div div p::text').get()
        print(product_name)

        # next_page = response.css('.wd-loop-footer products-footer nav ul li a::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

        # print(next_page)

        # product_data = []
        # product_data.append({
        #     'Name': product_name,
        #     'Price': product_price,
        #     'SKU': product_sku,
        #     'Description': product_description
        # })
            
        # print("name :", product_name)
        # print("price :", product_price)
        # print("sku :", product_sku)
        # print("description :", product_description)    

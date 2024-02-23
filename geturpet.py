from typing import Iterable
import scrapy
import pandas as pd
from scrapy.http import Request

class Geturpet(scrapy.Spider):
    name = 'geturpet'

    def start_requests(self):
        urls = ['https://geturpet.com/aquatic-plants/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links =[]
        product_divs = response.css('.product-inner')
        for product_div in product_divs:
            href = product_div.css('div a::attr(href)').get()
            links.append(href)
            print(href)
            
    #     for link in links:
    #         yield response.follow(link, callback=self.get_data)

    # def get_data(self, response):
    #     product_name = response.css('.product-summary-wrap div div h2::text').get()
    #     product_price = response.css('.price ins span bdi::text').get()
    #     if product_price is None:
    #         product_price = response.css('.price del span bdi::text').get()
    #     product_sku = response.css('.product_meta span span.sku::text').get()
    #     product_description = response.css('.woocommerce-tabs woocommerce-tabs-3r08z9lo resp-htabs p::text').get()
    #     product_availability = response.css('.product_meta span span.stock::text').get()
    #     if product_availability is None:
    #         product_availability = "Available"

    #     product_data = []
    #     product_data.append({
    #         'Name': product_name,
    #         'Price': product_price,
    #         'SKU': product_sku,
    #         'Description': product_description,
    #         'Availability': product_availability
    #     })

    #     print("name :", product_name)
    #     print("price :", product_price)
    #     print("sku :", product_sku)
    #     print("description :", product_description)
    #     print("Availability:", product_availability) 
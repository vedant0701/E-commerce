import scrapy 
import pandas as pd

class Greenwater(scrapy.Spider):
    name = ('greenwater')

    def start_requests(self):
        urls = ['https://ohmletshoppe.com/collections/4594']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        product_name = response.css('.CardTitle-sc-db3c384f-8.MdpCS::text').get()
        print(product_name)
    #     for link in links:
    #         yield response.follow(link, callback=self.get_data)

    # def get_data(self, response):
    #     product_name = response.css('.title-wrapper p::text').get()
        # product_price = response.css('.price ins span bdi::text').get()
        # if product_price is None:
        #     product_price = response.css('.price del span bdi::text').get()
        # product_sku = response.css('.product_meta span span.sku::text').get()
        # product_description = response.css('.woocommerce-tabs woocommerce-tabs-3r08z9lo resp-htabs p::text').get()
        # product_availability = response.css('.product_meta span span.stock::text').get()
        # if product_availability is None:
        #     product_availability = "Available"
        # print(product_name)
import scrapy
import pandas as pd

class ElysianFlora(scrapy.Spider):
    name = 'sreepadma'

    def start_requests(self):
        urls = ['https://www.sreepadma.com/all-plant']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = []
        product_divs = response.css('.product-card')
        for product_div in product_divs:
            href = product_div.css('a::attr(href)').get()
            links.append(href)
            
            
        for link in links:
            yield response.follow(link, callback=self.get_data)

        def get_data(self, response):
        product_name = response.css('.details-content h3 a::text').get()       
        product_price = response.css('.details-list-group table tr td::text').extract()[2]
        product_sku = response.css('.details-list-group table tr td::text').extract()[1]
        product_description = response.css('.product-details-frame div p::text').get()
       
        next_page = response.css('a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        
        product_data = []
        product_data.append({
            'Name': product_name,
            'Price': product_price,
            'SKU': product_sku,
            'Description': product_description
            
        })
        
        # print data 
        print("name :", product_name)
        print("price :", product_price)
        print("sku :", product_sku)
        print("description :", product_description)
        

        # # DataFrame 
        # df = pd.DataFrame(product_data)
        # print(df)
        # df.to_csv('product_data.csv', index=False) 


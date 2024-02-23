''' 
FLOW-
step 1 - using for loop iterate and obtain product link from 'https://fishykart.in/collections/aquarium-plants-online-india'
step 2 - use pagination to obtain all the links
step 3 - iterate links and obtain the data (name,price,categories,description)
step 4 - convert data into dataframe using pandas
step 5 - integrate dlt
'''
import scrapy
import pandas as pd
import dlt
class QuotesSpider(scrapy.Spider):
    name = "fishykart"

    start_urls = [
        "https://fishykart.in/collections/aquarium-plants-online-india"
    ]

    data = []

    def parse(self, response):
        # Follow the links to individual product pages
        product_links = response.css('div.grid-view-item.product-card a::attr(href)').extract()
        for product_link in product_links:
            yield response.follow(product_link, callback=self.parse_product)

        # Check for a next page link and follow it
        next_page = response.css('span.page a::attr(href)').extract()
        for page_link in next_page:
            yield response.follow(page_link, callback=self.parse)

    def parse_product(self, response):
        name = response.css('div.product-single__meta h1.product-single__title::text').get()
        price_ = response.css('div.price__sale dd span::text').get()
        if price_:
            price = price_.strip()
        product_sku = response.css('p.variant-sku::text').get()
        categories = response.css('ul.product-categories li a::text').getall()
        description_ = response.css('div#tab-1 ::text').getall()
        description = ' '.join(line.strip() for line in description_ if line.strip())

        # print("Product Title :", name)
        # print("price :",price)
        # print("SKU :", product_sku)
        # print("Categories :", categories)
        # print("description :",description)
        # print("------")
        # print("---")

        self.data.append({
            "Product Title": name,
            "Price": price,
            "SKU": product_sku,
            "Categories": categories,
            "Description": description
        })

    def closed(self, reason):
        json = self.DataFrame(self)  # Call the DataFrame method when the spider is closed
        # df = pd.DataFrame(json) # view dataframe
        # print(df)
        print(list(self.DataFrame(self)))

        self.fishykart_pipeline(df=json)

    @dlt.resource(
    table_name="fishykart_products",
    write_disposition="replace",
    )
    def DataFrame(self):
        df = pd.DataFrame(self.data)
        yield df.to_dict(orient='records')
        

    def fishykart_pipeline(self, df):
        pipeline = dlt.pipeline(
            pipeline_name="fishykart",
            destination='duckdb',
            dataset_name="fishykart_products",
        )
        load_info = pipeline.run(df)
        print(load_info)
        

if __name__ == "__main__":
    pass

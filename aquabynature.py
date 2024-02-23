import scrapy
import pandas as pd
import dlt

class AquabynatureSpider(scrapy.Spider):
    name = 'aquabynature'
    data = []

    start_urls = [
        "https://aquabynature-shop.com/59-aquatic-plants"
    ]

    def parse(self, response):
        # Extract product links and follow them
        product_divs = response.css('div.products.row div.product')
        for product_div in product_divs:
            product_link = product_div.css('a.product-thumbnail::attr(href)').get()
            if product_link:
                yield response.follow(product_link, callback=self.parse_product)

        # Pagination
        next_page = response.css('ul.page-list li.current + li a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        name = response.css('h1[itemprop="name"]::text').get()
        price = response.css('div.product-prices span::text').get()
        specifications_ = response.css('div.product-information div[id^="product-description-short-"]')
        specifications = ' '.join(specifications_.css('::text').extract())

        self.data.append({
            "Name": name,
            "Price": price,
            "Specifications": specifications
        })

    def closed(self, reason):
        print("Scrapy data:")
        json = self.DataFrame(self)  # Call the DataFrame method when the spider is closed
        # df = pd.DataFrame(json) # view dataframe
        # print(df)
        print(list(self.DataFrame(self)))

        self.aquabynature_pipeline(df=json)

    @dlt.resource(
    table_name="aquabynature_products",
    write_disposition="replace",
    )
    def DataFrame(self):
        df = pd.DataFrame(self.data, columns=["Name", "Price", "Specifications"])
        yield df.to_dict(orient='records')
        

    def aquabynature_pipeline(self, df):
        pipeline = dlt.pipeline(
            pipeline_name="aquabynature",
            destination='duckdb',
            dataset_name="aquabynature_products",
        )
        load_info = pipeline.run(df)
        print(load_info)
        
        

if __name__ == "__main__":
    pass
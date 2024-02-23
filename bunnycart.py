import scrapy
import pandas as pd
import dlt

class BunnycartSpider(scrapy.Spider):
    name = 'bunnycart'
    start_urls = ['https://www.bunnycart.com/aquarium-plants']

    data = []

    def parse(self, response):
        # Select the <ol> element containing the list of products
        ol = response.css('ol.filterproducts.products.list.items.product-items.has-qty li.item.product.product-item')

        for li in ol:
            product_name_ = li.css('strong.product.name.product-item-name a::text').get()
            product_name = product_name_.strip()
            product_price = li.css('span.price-container span.price-wrapper span.price::text').get()
            rating = li.css('div.rating-result::attr(title)').get()

            self.data.append({
                'Name': product_name,
                'Price': product_price,
                'Ratings': rating
            })

        # Pagination
        next_page = response.css('li.item.pages-item-next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        json = self.DataFrame(self)  # Call the DataFrame method when the spider is closed
        # df = pd.DataFrame(json) # view dataframe
        # print(df)
        print(list(self.DataFrame(self)))

        self.bunnycart_pipeline(df=json)

    @dlt.resource(
    table_name="bunnycart_products",
    write_disposition="replace",
    )
    def DataFrame(self):
        df = pd.DataFrame(self.data)
        yield df.to_dict(orient='records')
        
    def bunnycart_pipeline(self, df):
        pipeline = dlt.pipeline(
            pipeline_name="bunnycart",
            destination='duckdb',
            dataset_name="bunnycart_products",
        )
        load_info = pipeline.run(df)
        print(load_info)
        
        

if __name__ == "__main__":
    pass
        
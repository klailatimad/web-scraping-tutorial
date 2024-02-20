# Import all the necessary libraries
import scrapy
from dotenv import load_dotenv
import os

class FarFetchWomenUrlsSpider(scrapy.Spider):

    load_dotenv() # Load the .env file so that we can obtain the Scraper API credentials.

    name = "farfetch_women_get_urls" # Provide your spider a unique name. We will call this spider by the name in the terminal.

    headers = {
            'Content-Type': 'application/json',
            # Add any additional headers as needed
        }
    
    api_key = os.getenv('Scraper_API_Key') # Retrieve the scraper API key
    
    m = 1 # Page number count. We will use this variable to increment the pages
    
    def start_requests(self):

        '''
        This function traverses through each subfilter we want to loop through
        '''

        # Provide the url to start the crawl
        start_urls = [
            'https://www.farfetch.com/ca/shopping/women/watches-analog-1/items.aspx?page=1&view=96&sort=2&q=Watches',
        ]
        
        # Converts the start url to be used by Scraper API
        start_urls_scraper_api = [f'http://api.scraperapi.com/?api_key={self.api_key}&url={url}' for url in start_urls]

        # For each start url (in this case there is only one), we will run the parse function
        for url in start_urls_scraper_api:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):

        '''
        This function collects all the item urls in each page
        '''

        # Gets the item page urls
        rel_urls = response.xpath('//li[@data-testid="productCard"]/descendant::a/@href').getall()
        
        # Because the item page urls are relative paths, we will convert to the absolute path
        urls = ['https://www.farfetch.com' + url for url in rel_urls]

        # For each item url, we will store it in a csv file
        for url in urls:
            yield {'watch_url': url}
        
        # If there exists item urls in the current page, we will increment to scrape the next page. 
        # Otherwise, we will stop the scrape as we will have run out of item urls to scrape.
        if urls:
            # Increment the page number to reflect the next page
            self.m += 1 
            # Create the next page url
            next_page = f'https://www.farfetch.com/ca/shopping/women/watches-analog-1/items.aspx?page={self.m}&view=96&sort=2&q=Watches'
            # Convert the next page url to be usable by Scraper API
            next_page_scraper_api_url = f'http://api.scraperapi.com/?api_key={self.api_key}&url={next_page}'
            # Scrape the next page
            yield scrapy.Request(url=next_page_scraper_api_url, headers=self.headers, callback=self.parse)
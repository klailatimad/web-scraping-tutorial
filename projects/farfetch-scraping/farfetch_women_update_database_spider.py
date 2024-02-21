import scrapy
from datetime import *
import uuid
from dotenv import load_dotenv
import pandas as pd
import os

class FarFetchWomenUpdateDBSpider(scrapy.Spider):

    load_dotenv() # Load the .env file

    name = "farfetch_women_update_database" # Create a unique name for your spider so that we could call it accordingly in the terminal

    headers = {
            'Content-Type': 'application/json',
            # Add any additional headers as needed
        }
    
    api_key = os.getenv('Scraper_API_Key') # Retrieve the scraper API key
    
    # Gets the urls from the csv file (referred as "current scrape") that we generated using the get_urls spider
    # Please note you may need to rename the directory you want to retrieve your csv file from
    # depending on where you saved the files
    if os.path.exists('farfetch_new_existing_deleted/FarFetch_Women_Urls.csv'): # If the file exists we load it
        current_scrape_df = pd.read_csv('farfetch_new_existing_deleted/FarFetch_Women_Urls.csv').drop_duplicates(subset=['watch_url'])
    else: # If the file doesn't exist we create an empty dataframe
        current_scrape_df = pd.DataFrame(columns=['watch_url'])

    # Only if an existing database of scrapes exists we do the following:
    if os.path.exists('farfetch_new_existing_deleted/FarFetch_Women_Total.csv'):
        
        # Compare the current scrape urls to the urls of our existing database
        existing_df = pd.read_csv('farfetch_new_existing_deleted/FarFetch_Women_Total.csv')
        merged_df = pd.merge(existing_df, current_scrape_df, on='watch_url', how='outer', indicator=True)

        # Updates the timestamp and status column for urls that exist in our existing database but not the current scrape
        deleted_df = merged_df[merged_df['_merge']=='left_only']
        deleted_df['time_updated'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000')
        deleted_df['status'] = 'Deleted'
        deleted_df.drop(columns=['_merge'], inplace=True)
        deleted_df.to_csv('farfetch_new_existing_deleted/FarFetch_Women_Deleted.csv', index=False)

        # Updates the timestamp and status column for urls that exist in our existing database AND the current scrape
        existing_df = merged_df[merged_df['_merge']=='both']
        existing_df['time_updated'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000')
        existing_df['status'] = 'Existing'
        existing_df.drop(columns=['_merge'], inplace=True)
        existing_df.to_csv('farfetch_new_existing_deleted/FarFetch_Women_Existing.csv', index=False)

        # Identify the urls that doesn't exist in the existing database but exists in the current scrape
        new_df = merged_df[merged_df['_merge']=='right_only']
        urls_to_scrape = new_df['watch_url'].tolist()
    
    else:
        # If there is no existing database of scrapes, then we scrape all the urls we collected in the current scrape
        urls_to_scrape = current_scrape_df['watch_url'].tolist()

    def start_requests(self):

        '''
        This function traverses each url that we want to scrape
        '''

        # Converts the list of urls to scrape to be usable by Scraper API
        start_urls = [f'http://api.scraperapi.com/?api_key={self.api_key}&url={url}' for url in self.urls_to_scrape]

        # Scrapes all the urls in the parse function
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        '''
        This function scrapes the fields for each item url. Please note that because each website has a different HTML structure,
        the code shown here will likely not be applicable to another website that you scrape. I built out the code for this function
        by inspecting the HTML of the item url pages.
        '''
        
        # Create an empty dictionary (to be stored in a csv file later)
        item_dict = {}

        # Creates a timestamp
        item_dict['time_updated'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000')
        
        # Obtain a reference number
        reference_number = response.xpath('//div[@class="ltr-92qs1a"]/p[contains(text(),"Brand style ID")]/span/text()').get()
        # If the reference number exists in the item url scrape, we clean it.
        if reference_number:
            item_dict['reference_number'] = reference_number.strip()
        # Otherwise, we leave the reference number blank
        else:
            item_dict['reference_number'] = ''
        brand = response.xpath('//h1[@class="ltr-i980jo el610qn0"]/a/text()').get()
        # If the brand doesn't exist, instead of leaving it as a "None" type, we leave it as a blank string
        if not brand:
            brand = ''
        # Retrieve the short description
        short_description = response.xpath('//p[@data-testid="product-short-description"]/text()').get()
        # If the short description doesn't exist, instead of leaving it as a "None" type, we leave it as a blank string
        if not short_description:
            short_description = ''
        # In this case, the listing title is the combination of the brand and short description. This may vary depending on the item page structure
        item_dict['listing_title'] = brand + ' ' + short_description
        # Obtain the url of the watch. Because we are using scraper api url, we will obtain the string after "url="
        item_dict['watch_url'] = response.url.split('url=')[-1]
        # Unique id for the scrape instance
        item_dict['unique_id'] = str(uuid.uuid4()).replace('-', '')
        item_dict['source'] = 'FarFetch'
        item_dict['brand'] = brand
        price = response.xpath('//p[@data-component="PriceLarge"]/text()').get()
        # If the price exists
        if price:
            item_dict['currency'] = price[0] # Extract the currency (eg. $)
            price_raw = price.split('.')[0][1:] # Gets the value before the decimal place (eg. $400.00 -> 400)
            item_dict['price'] = ''.join(i for i in price_raw if i.isdigit()) # Removes all non digit values such as commas
        # Otherwise leave it blank
        else:
            item_dict['currency'] = ''
            item_dict['price'] = ''
        # Gets the url link for the image
        item_dict['image_url'] = response.xpath('//div[@class="ltr-bjn8wh ed0fyxo0"]/descendant::img/@src').get()
        item_dict['contents'] = ''
        item_dict['seller_name'] = 'FarFetch'
        item_dict['seller_link'] = 'https://aboutfarfetch.com/?_gl=1*1o8i8sg*_ga*MTU4MjU2ODEyNC4xNzA2ODA0OTE3*_ga_CEF7PMN9HX*MTcwNjgwNDkxNy4xLjEuMTcwNjgwNDk4MC41Ny4wLjA.*_fplc*ZU0lMkJzcFRWRUpnakZESm9QaTd6T0hTMWtZS3I1VXcxUSUyQjM4UW5NNDdxN1JoJTJGaGV6ZnVBUFFxdyUyQm9Kd0wxYTNWbWMyYlNjbDQxVnRkdHZHVUNEd2htRzMxNjNBS0FSVndacmpuRm5oTUQ0ZlNqWDExWG9BRzJZM3Q1cCUyRnV2USUzRCUzRA..&_ga=2.255924171.1313828267.1706804917-1582568124.1706804917'
        item_dict['country'] = ''
        item_dict['seller_type'] = 'Retailer'
        # Gets the text for the listing button (eg. "Add to cart")
        listing_type = response.xpath('//button[@class="ltr-twjh4c"]/span/text()').get()
        if listing_type=='Add To Bag':
            item_dict['listing_type'] = 'Buy it Now'
        else:
            item_dict['listing_type'] = listing_type
        # Gets the text under the "Highlights" section of the page
        highlights = response.xpath('//li[@class="ltr-4y8w0i-Body"]/text()').getall()
        # If the bullet point under "Highlights" contains "This piece", then it is stating what the condition of the item is.
        # We then remove "This piece is " to clean this field up
        condition_raw = [row.replace('This piece is ','') for row in highlights if 'This piece' in row]
        if condition_raw:
            condition = condition_raw[0].strip()
        else:
            condition = ''
        item_dict['condition'] = condition
        item_dict['year_of_production'] = ''
        item_dict['decade_of_production'] = ''
        item_dict['year_introduced'] = ''
        item_dict['parent_model'] = ''
        item_dict['specific_model'] = ''
        item_dict['nickname'] = ''
        item_dict['marketing_name'] = ''
        item_dict['style'] = ''
        item_dict['serial_number'] = ''
        item_dict['type'] = ''
        item_dict['made_in'] = ''
        item_dict['specific_location'] = ''
        item_dict['shipping_notes'] = 'One delivery fee to most locations (check our Orders & Delivery page) \
Free returns within 14 days (excludes final sale and made-to-order items, face masks and certain products containing hazardous or flammable materials, such as fragrances and aerosols)'
        item_dict['seller_rating'] = ''
        item_dict['case_shape'] = ''
        # If the word "case" is in the bullet point under "Highlights" section, this is describing the case material
        # We then remove "case" to clean this field up
        case_material_raw = [row.replace('case', '') for row in highlights if 'case' in row]
        if case_material_raw:
            case_material = case_material_raw[0].strip()
        else:
            case_material = ''
        item_dict['case_material'] = case_material
        item_dict['case_finish'] = ''
        item_dict['caseback'] = ''
        # If the text "mm" is in the bullet point under "Highlights" section, this is describing the diameter
        # We then remove "mm" to clean this field up
        diameter_raw = [row for row in highlights if 'mm' in row]
        if diameter_raw:
            diameter = diameter_raw[0].strip()
        else:
            diameter = ''
        item_dict['diameter'] = diameter
        item_dict['between_lugs'] = ''
        item_dict['lug_to_lug'] = ''
        item_dict['case_thickness'] = ''
        item_dict['bezel_material'] = ''
        item_dict['bezel_color'] = ''
        # If the word "glass" is in the bullet point under "Highlights" section, this is describing the crystal field
        # We then remove "glass" to clean this field up
        crystal_raw = [row for row in highlights if 'glass' in row]
        if crystal_raw:
            crystal = crystal_raw[0].strip()
        else:
            crystal = ''
        item_dict['crystal'] = crystal
        # If the text "ATM" is in the bullet point under "Highlights" section, this is describing the water resistance
        # We then remove "water resistance" to clean this field up
        water_resistance_raw = [row.replace('water resistance', '') for row in highlights if 'ATM' in row]
        if water_resistance_raw:
            water_resistance = water_resistance_raw[0].strip()
        else:
            water_resistance = ''
        item_dict['water_resistance'] = water_resistance
        item_dict['weight'] = ''
        item_dict['dial_color'] = ''
        item_dict['numerals'] = ''
        # If the text "strap" is in the bullet point under "Highlights" section, this is describing the bracelet material
        # We then remove "strap" to clean this field up
        bracelet_material_raw = [row.replace('strap', '') for row in highlights if 'strap' in row]
        if bracelet_material_raw:
            bracelet_material = bracelet_material_raw[0].strip()
        else:
            bracelet_material = ''
        item_dict['bracelet_material'] = bracelet_material
        item_dict['bracelet_color'] = ''
        # If the text "clasp" is in the bullet point under "Highlights" section, this is describing the clasp type
        clasp_type_raw = [row for row in highlights if 'clasp' in row]
        if clasp_type_raw:
            clasp_type = clasp_type_raw[0].strip()
        else:
            clasp_type = ''
        item_dict['clasp_type'] = clasp_type
        # If the text "movement" is in the bullet point under "Highlights" section, this is describing the movement field
        movement_raw = [row for row in highlights if 'movement' in row]
        if movement_raw:
            movement = movement_raw[0].strip()
        else:
            movement = ''
        item_dict['movement'] = movement
        item_dict['caliber'] = ''
        item_dict['power_reserve'] = ''
        item_dict['frequency'] = ''
        item_dict['jewels'] = ''
        item_dict['features'] = ''
        item_dict['status'] = 'New' # For any url that uses this function, it is a "New" link to update to our database

        yield item_dict # Saving the dictionary to a csv file. Each time we call this function, 
        # we save to a row in the csv file that we designate

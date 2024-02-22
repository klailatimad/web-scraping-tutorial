import requests
import json
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import urljoin
import uuid
from datetime import datetime
import pandas as pd
from time import sleep
import httpx
import asyncio
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings("ignore")
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set-up Chrome-Driver for Selenium
def get_webdriver():
    s = Service('chromedriver\\chromedriver.exe')
    options = Options()
    options.binary_location = 'chrome\\chrome.exe'
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.200 Safari/537.36 Edge/16.16299')
    options.add_argument("--force-device-scale-factor=0.75")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options,service=s)
    return driver

# Close pop-up window on homepage
def close_pop_up():
    try:
        WebDriverWait(driver, 3).until( # WebDriverWait(driver,seconds to wait).until(something happens)
            EC.presence_of_element_located((By.CLASS_NAME, 'button.button--primary.button--full.disabled.newsletter-input__signup-btn'))
        ) # EC.presence_of_element_located() to check if certain element is foundable
        button = driver.find_element(By.CLASS_NAME,'modal__headline') \
                       .find_element(By.CLASS_NAME,'mobileheader__close') # driver..find_element()/find_elements() most commonly used
        button.click() # .click() act as the action you (left)click your mouse
    except:
        pass # try/except: try execute something; except error occurs, execute something under 'except:'

# Find the last page number
def get_last_page_aw():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'pagination__item.pagination__item--next'))
     )
    for i in range(1,4):
        try :
            last_page = int(driver.find_element(By.CLASS_NAME,'pagination__item.pagination__item--next')
                              .find_element(By.XPATH,'preceding-sibling::*[1]').text) # element.text, get the text
            break
        except:
            print(f'retrying... {i} of 3')
            sleep(1) # time.sleep(seconds to pause)
    return last_page

# Collect all pages' URLs and saved to a list
def get_all_page_urls_aw():
    base_url = 'https://www.chronext.com/buy?s%5Bef5bfee0-c7d4-470e-82e2-39d397cb3750%5D%5Boffset%5D='
    last_p = get_last_page_aw()
    print(f'Total page of {last_p}')
    page_urls = [base_url+str(i*24) for i in range(last_p)] # list comprehension
    return page_urls

# Open the dropdown menu and switch to chosen country and currency
def change_country_currency(abbv='US'):
    '''Open the dropdown menu and switch to US USD'''
    driver.find_element(By.CLASS_NAME,'language-switcher').click()
    button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'input-select-component'))
             )
    button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'css-1gdpjst-menu'))
    )
    option_tags = driver.find_element(By.CLASS_NAME,'css-1gdpjst-menu') \
                        .find_elements(By.CLASS_NAME,'language-switcher__content--country-option')
    for tag in option_tags:
        if tag.find_element(By.TAG_NAME,'span').get_attribute('title') == abbv:
            tag.click()
            break
    driver.find_element(By.CLASS_NAME,'btn.btn--success.btn--full.language-switcher-footer__buttons--save-btn').click()

# Fetch product URLs on current page    
def get_current_listing_aw(page_url):
    page_select = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'pagination__list'))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'end'});", page_select) 
    # Excute JavaScript: scroll to the bottom of the element will be aligned with the bottom of the scrollable area
    sleep(0.5)
    tags = driver.find_elements(By.CLASS_NAME,'product-tile')
    current_page_listing = [tag.find_element(By.TAG_NAME,'a').get_attribute('href') for tag in tags]
    return current_page_listing

# Add retry function to fetch product URLs on current page if page not loaded properly
def get_current_listing_retry_aw(page_url):
    driver.get(page_url)
    current_page_listing = get_current_listing_aw(page_url)
    i = 0
    if len(current_page_listing) != 24 and i < 3:
        current_page_listing = get_current_listing_aw(page_url)
        i += 1
        if i > 1:
            print(f'retrying...{i} of 3')
    else:
        current_page_listing = get_current_listing_aw(page_url)
        pass
    return current_page_listing

# Loop the 'Fetch product URLs on current page' funtion for all page URLs to get all product URLs on all pages to a list
def get_product_listing_aw(page_url_list):
    product_listing=[]
    for page_url in page_url_list:
        
        product_listing.extend(get_current_listing_retry_aw(page_url)) # extend the list
        print(f'{page_url_list.index(page_url)+1} of {len(page_url_list)} are done.')
    return product_listing

'''Async get soup'''
# async running getting soup
async def async_request_and_parse(url):
    async with httpx.AsyncClient(timeout=200) as client:
        # Make an asynchronous GET request
        response = await client.get(url) # Most regular way: response = request.get(url)


        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser') # soup = BeautifulSoup(html, 'html.parser')
            return soup
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            
async def async_scrape(url):  

    for i in range(1,4):
        try:
            soup = await async_request_and_parse(url)
            break
        except:

            print(f'retrying... {i} of 3 ')
            sleep(1)
    try:
        blocks = soup.find('div',class_='product-specifications-accordion') \
                 .find_all('div',class_='accordion-item__title-wrapper')  # soup.find/find_all('html_tag_type',class_/other attribute='')
        spec_dict = {}
        for block in blocks:
            tags = block.find_next_sibling().find_all('div',class_='specification__wrapper') # tag.find_next_sibling(), find next tag
            if block.text == 'Features':
                features = [tag.find('div',class_='specification__value').text for tag in tags] # tag.text, get the text
                spec_dict['Features'] = ', '.join(features)
            else:
                for tag in tags:
                    spec_dict[tag.find('div',class_='specification__title').text] = tag.find('div',class_='specification__value').text
    except:
        pass
    field_list = ['reference_number',
                 'listing_title',
                 'watch_URL',
                 'unique_id',
                 'source',
                 'brand',
                 'currency',
                 'price',
                 'image_URL',
                 'contents',
                 'seller_name',
                 'seller_link',
                 'country',
                 'seller_type',
                 'listing_type',
                 'condition',
                 'year_of_production',
                 'decade_of_production',
                 'year_introduced',
                 'parent_model',
                 'specific_model',
                 'nickname',
                 'marketing_name',
                 'style',
                 'serial_number',
                 'type',
                 'made_in',
                 'specific_location',
                 'shipping_notes',
                 'seller_rating',
                 'case_shape',
                 'case_material',
                 'case_finish',
                 'caseback',
                 'diameter',
                 'between_lugs',
                 'lug_to_lug',
                 'case_thickness',
                 'bezel_material',
                 'bezel_color',
                 'crystal',
                 'water_resistance',
                 'weight',
                 'dial_color',
                 'numerals',
                 'bracelet_material',
                 'bracelet_color',
                 'clasp_type',
                 'movement',
                 'caliber',
                 'power_reserve',
                 'frequency',
                 'jewels',
                 'features']
    field_dict = {field: [] for field in field_list}
    
    # reference_number
    try:
        key = 'reference_number'
        field_dict[key].append(spec_dict['Reference'])
    except:
        field_dict[key].append(None) 
    # listing_title
    try:
        key = 'listing_title'
        field_dict[key].append(soup.find('h1',class_='product-stage__title').text)
    except:
        field_dict[key].append(None) 
    # watch_URL
    try:
        key = 'watch_URL'
        field_dict[key].append(url)
    except:
        field_dict[key].append(None)
    # unique_id
    try:
        key = 'unique_id'
        field_dict[key].append(str(uuid.uuid4()).replace('-',''))
    except:
        field_dict[key].append(None)
    # source 
    try:
        key = 'source'
        field_dict[key].append('Chronext')
    except:
        field_dict[key].append(None)           
    # brand 
    try:
        key = 'brand'
        field_dict[key].append(spec_dict['Brand'])
    except:
        field_dict[key].append(None)   
    # currency 
    try:
        key = 'currency'
        field_dict[key].append('USD')
    except:
        field_dict[key].append(None)
    # price
    try:
        key = 'price'
        price_tag = soup.find('div',class_='price').text       
        field_dict[key].append(''.join(re.findall('\d+',price_tag))) # re.findall('pattern',string), regex
    except:
        field_dict[key].append(None)
    # image_URL
    try:
        key = 'image_URL'
        field_dict[key].append(soup.find('div','product-stage').find('img')['src']) # tag.find(xxx)['attribute']
    except:
        field_dict[key].append(None) 
    # contents
    try:
        key = 'contents'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None) 
    # seller_name
    try:
        key = 'seller_name'
        field_dict[key].append('Chronext')
    except:
        field_dict[key].append(None) 
    # seller_link
    try:
        key = 'seller_link'
        field_dict[key].append('https://www.chronext.com/about-us')
    except:
        field_dict[key].append(None) 
    # country
    try:
        key = 'country'
        country_tag = soup.find('div','delivery-info__label delivery-info__label--popout').text      
        field_dict[key].append(re.findall('Free try-on in our (\w+) Lounges',country_tag)[0])
    except:
        field_dict[key].append(None)
    # seller_type
    try:
        key = 'seller_type'
        field_dict[key].append('Dealer')
    except:
        field_dict[key].append(None) 
    # listing_type
    try:
        key = 'listing_type'
        field_dict[key].append(soup.find('button','btn btn--success btn--with-icon btn--full product-stage__buttons-add-to-cart').text)
    except:
        field_dict[key].append(None) 
    # condition 
    try:
        key = 'condition'
        field_dict[key].append(spec_dict['Condition'])
    except:
        field_dict[key].append(None)               
    # year_of_production 
    try:
        key = 'year_of_production'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)   
    # decade_of_production 
    try:
        key = 'decade_of_production'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)   
    # year_introduced 
    try:
        key = 'year_introduced'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)  
    # parent_model
    try:
        key = 'parent_model'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None) 
    # specific_model 
    try:
        key = 'specific_model'
        field_dict[key].append(spec_dict['Model'])
    except:
        field_dict[key].append(None)             
    # nickname 
    try:
        key = 'nickname'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # marketing_name 
    try:
        key = 'marketing_name'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)            
    # style 
    try:
        key = 'style'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # serial_number 
    try:
        key = 'serial_number'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None) 
    # type 
    try:
        key = 'type'
        field_dict[key].append(spec_dict['Gender'])
    except:
        field_dict[key].append(None)         
    # made_in 
    try:
        key = 'made_in'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # specific_location 
    try:
        key = 'specific_location'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # shipping_notes 
    try:
        key = 'shipping_notes'
        field_dict[key].append('We offer free shipping worldwide.')
    except:
        field_dict[key].append(None)
    # seller_rating 
    try:
        key = 'seller_rating'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # case_shape      
    try:
        key = 'case_shape'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # case_material    
    try:
        key = 'case_material'
        field_dict[key].append(spec_dict['Case'])
    except:
        field_dict[key].append(None)   
    # case_finish 
    try:
        key = 'case_finish'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)           
    # caseback    
    try:
        key = 'caseback'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # diameter
    try:
        key = 'diameter'
        field_dict[key].append(spec_dict['Dimensions'])
    except:
        field_dict[key].append(None) 
    # between_lugs 
    try:
        key = 'between_lugs'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # lug_to_lug 
    try:
        key = 'lug_to_lug'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # case_thickness
    try:
        key = 'case_thickness'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)            
    # bezel_material 
    try:
        key = 'bezel_material'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # bezel_color 
    try:
        key = 'bezel_color'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # crystal  
    try:
        key = 'crystal'
        field_dict[key].append(spec_dict['Crystal'])
    except:
        field_dict[key].append(None)

    # water_resistance 
    try:
        key = 'water_resistance'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)            
    # weight 
    try:
        key = 'weight'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # dial_color 
    try:
        key = 'dial_color'
        field_dict[key].append(spec_dict['Dial Color'])
    except:
        field_dict[key].append(None)       
    # numerals 
    try:
        key = 'numerals'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)
    # bracelet_material  
    try:
        key = 'bracelet_material'
        field_dict[key].append(spec_dict['Bracelet'])
    except:
        field_dict[key].append(None)  
    # bracelet_color 
    try:
        key = 'bracelet_color'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None) 
    # clasp_type
    try:
        key = 'clasp_type'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)      
    # movement
    try:
        key = 'movement'
        field_dict[key].append(spec_dict['Movement'])
    except:
        field_dict[key].append(None)  
    # caliber 
    try:
        key = 'caliber'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)             
    # power_reserve 
    try:
        key = 'power_reserve'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)  
    # frequency 
    try:
        key = 'frequency'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)           
    # jewels 
    try:
        key = 'jewels'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None) 
    # features 
    try:
        key = 'features'
        field_dict[key].append(None)
    except:
        field_dict[key].append(None)   
 
    return field_dict

async def scrape_task_batch(url_list):
    results_dict = {}
    # Create a list of tasks for asynchronous requests
    tasks = [async_scrape(url) for url in url_list]
    batch_size = 20
    # Iterate over batches and gather results
    for i in range(0, len(url_list), batch_size):
        batch = tasks[i:i + batch_size]
        print(f'Start to scrape {i}:{i + batch_size} of {len(url_list)}')
        gathered_results = await asyncio.gather(*batch)
        for result_dict in gathered_results:
            for index, result_list in result_dict.items():
                if index in results_dict:
                    results_dict[index].extend(result_list)
                else:
                    results_dict[index] = result_list
                
    return results_dict

# by using if __name__ == '__main__':, you can write code that will only be executed when the script is run directly, 
# not when it's imported as a module into another script
if __name__ == '__main__':
    driver = get_webdriver() # set-up chrome-driver for selenium, open the Chrome
    driver.get('https://www.chronext.com/buy?s%5Bef5bfee0-c7d4-470e-82e2-39d397cb3750%5D%5Boffset%5D=0') # go to the homepage
    sleep(10)
    close_pop_up()
    sleep(3)
    change_country_currency(abbv='US') #abbv option can be found at 'country_currency_abbv.json'
    sleep(5)
    # get all pages urls
    page_urls_aw = get_all_page_urls_aw()
    # get all product urls
    product_listing_aw = get_product_listing_aw(page_urls_aw)
    driver.quit() # close the Chrome
    # async scrape all product pages
    final_dict_aw = asyncio.run(scrape_task_batch(product_listing_aw))
    df_aw = pd.DataFrame(final_dict_aw) # turn the dictionary into a Pandas DataFrame
    today_date = datetime.today().strftime('%m/%d/%y') # get the today's date, datetime.now().strftime("%Y-%m-%d %H:%M:%S %z") to get current time and date
    df_aw.insert(0, 'time_updated', today_date) # insert a new column into the position '0', which is the very first column
    df_aw.to_csv('Chronext_listing.csv',index=False) # save the Pandas DataFrame into a csv file in the current folder


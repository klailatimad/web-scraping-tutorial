## Project Setup
1. Inside your terminal, run the following to set up your environment:
a. Run "sudo apt update" <br>
b. "sudo apt install python3-pip" <br>
c. "sudo apt install python3-scrapy" <br>
d. "pip install Scrapy==2.11.0" <br>
e. "pip install scraperapi-sdk==0.2.2" <br>
f. "pip install python_dotenv==1.0.0" <br>
g. "pip install pandas==1.3.5" <br>
2. Run "scrapy startproject {project name}" inside the directory you wish to store this scrapy project in. <br>
3. You may need to run the following if you get the following error: "AttributeError: module 'lib' has no attribute 'OpenSSL_add_all_algorithms'" <br>
a. python3 -m pip install --upgrade cryptography pyOpenSSL <br>
b. sudo apt-get install libssl-dev <br>
4. Once you have created a `Scrapy` project, put the Python files from this directory into the spiders folder in your own directory. Each `Scrapy` project has a spiders folder automatically (assuming we completed the `Scrapy` project step correctly). <br>
5. Inside the settings.py file (which gets automatically created in each `Scrapy` project), make sure the fields are set as following: <br>
a. "HTTPERROR_ALLOWED_CODES = [401, 404, 405]" <br>
b. "ROBOTSTXT_OBEY = False" <br>
c. "DOWNLOAD_DELAY = 0.5" (May need to set it to 1 if 0.5 overwhelms the site server) <br>
d. 'USER_AGENT = "Mozilla/5.0"' <br>
e. "CONCURRENT_REQUESTS = 32" <br>
f. "CONCURRENT_REQUESTS_PER_DOMAIN = 32" <br>
g. "CONCURRENT_REQUESTS_PER_IP = 16" <br>
h. "COOKIES_ENABLED = False" <br>
6. In the directory where you will be running your scrapy spiders, do the following: <br>
a. Create a .env file <br>
b. Inside the .env file, add the following line: <br>
Scraper_API_Key='{enter Scraper API key}' <br>

## Running web scrape
1. To retrieve the urls, run the following: <br>
`scrapy crawl farfetch_women_get_urls -o farfetch_new_existing_deleted/FarFetch_Women_Urls.csv -t csv` <br>
The spider name is "farfetch_women_get_urls", so we call this immediately after "scrapy crawl" <br>
-o: csv file directory to save your scrape <br>
-t: specify the output format, in our case, csv <br>
3. To run a scrape for the item urls, run the following: <br>
`scrapy crawl farfetch_women_update_database -o farfetch_new_existing_deleted/FarFetch_Women_New.csv -t csv`<br>
4. If there's an error running the scrapy spiders, make sure twisted version is 21.7.0 and scrapy version is 2.11.0 <br>

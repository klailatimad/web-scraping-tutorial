## Scrapy Setup
Inside your terminal, run the following:
a. Run "sudo apt update" <br>
b. "sudo apt install python3-pip" <br>
c. "sudo apt install python3-scrapy" <br>
d. "pip install Scrapy==2.11.0" <br>
e. "pip install scraperapi-sdk==0.2.2" <br>
f. "pip install python_dotenv==1.0.0" <br>
g. "pip install pandas==1.3.5" <br>
Please refer to [this link](https://github.com/klailatimad/web-scraping-tutorial/blob/main/docs/introduction-to-scrapy.md) to set up the `Scrapy` project after setting up the Scrapy environment. <br>
Once you have created a `Scrapy` project, put the Python files from this directory into the spiders folder in your own directory. Each `Scrapy` project has a spiders folder automatically (assuming we completed the `Scrapy` project step correctly). <br>
Inside the settings.py file (which gets automatically created in each `Scrapy` project), make sure the fields are set as following: <br>
a. "HTTPERROR_ALLOWED_CODES = [401, 404, 405]" <br>
b. "ROBOTSTXT_OBEY = False" <br>
c. "DOWNLOAD_DELAY = 0.5" (May need to set it to 1 if 0.5 overwhelms the site server) <br>
d. 'USER_AGENT = "Mozilla/5.0"' <br>
e. "CONCURRENT_REQUESTS = 32" <br>
f. "CONCURRENT_REQUESTS_PER_DOMAIN = 32" <br>
g. "CONCURRENT_REQUESTS_PER_IP = 16" <br>
h. "COOKIES_ENABLED = False" <br>

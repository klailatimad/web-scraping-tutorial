## Scrapy Setup
Please refer to [this link](https://github.com/klailatimad/web-scraping-tutorial/blob/main/docs/setting-up-environment.md) to set up the `Scrapy` environment. <br>
Please refer to [this link](https://github.com/klailatimad/web-scraping-tutorial/blob/main/docs/introduction-to-scrapy.md) to set up the `Scrapy` project after setting up the Scrapy environment. <br>
Once you have created a `Scrapy` project, put the Python files from this directory into the spiders folder in your own directory. Each `Scrapy` project has a spiders folder automatically (assuming we completed the `Scrapy` project step correctly). <br>
Inside the settings.py file (which gets automatically created in each `Scrapy` project), make sure the fields are set as following: <br>
a. "HTTPERROR_ALLOWED_CODES = [401, 404, 405]"
b. "ROBOTSTXT_OBEY = False"
c. "DOWNLOAD_DELAY = 0.5" (May need to set it to 1 if 0.5 overwhelms the site server)
d. 'USER_AGENT = "Mozilla/5.0"'
e. "CONCURRENT_REQUESTS = 32"
f. "CONCURRENT_REQUESTS_PER_DOMAIN = 32"
g. "CONCURRENT_REQUESTS_PER_IP = 16"
h. "COOKIES_ENABLED = False"

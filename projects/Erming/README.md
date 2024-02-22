# Example for Webscraping with BeautifulSoup and Selenium
## Chronext Scraping
url = https://www.chronext.com/buy?s%5Bef5bfee0-c7d4-470e-82e2-39d397cb3750%5D%5Boffset%5D=
### Scrape Process
1. Fetch all URLs for detailed product pages 
2. Fetch all field on each detailed product page
3. Save as csv file
### Reason to use Selenium
For product listing pages, getting the html using `request.get(url)` can not achieve the proper elements(tags) with the detailed product page URLs. Website contains Javascript that can not be fetched by simply `request` libraries. We use `Selenium` with `Chromedriver` here to be able to fetch the content we need. The size of the website is small, for large website, we may consider using `Proxy` to fetch JavaScript content since Selenium will use a lot RAM and comparably slow.
But if the website contains element need interaction(button, drop-down list...), `Selenium` would still be one of the best tool to use.
### Reason to use BeautifulSoup combined
As said before, `Selenium` is useful but slow. To increase the efficiency, we should always consider `BeautifulSoup` rather than `Selenium` if possible. Since in each detailed product pages, we are able to fetch html with `BeautifulSoup`(`request`)
### Extra methods to improve efficiency
- Async (send multiple requests without waiting for response one by one)
- Multi-threading (take advantage of using multiple CPU cores to handle tasks, Python by default only use 1 core)
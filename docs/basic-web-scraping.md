

## 2. Basic Web Scraping with `requests` and `BeautifulSoup`

Before we explore the advanced features of Scrapy and Selenium, it's essential to understand the fundamentals of web scraping with Python using simpler libraries like `requests` and `BeautifulSoup`. This approach is often sufficient for basic scraping tasks and serves as a great introduction to the data extraction process.

### What are `requests` and `BeautifulSoup`?

-   **`requests`:** The `requests` library is a Python HTTP library that's simple and elegant. It allows you to send HTTP/1.1 requests extremely easily without needing to manually add query strings to your URLs or form-encode your POST data.
    
-   **`BeautifulSoup`:** BeautifulSoup is a Python library for parsing HTML and XML documents. It's often used for web scraping because it can handle different parsers and navigate or search the parse tree.
    

### Installation

To get started, you need to install both libraries. You can do this via `pip`:
```sh
pip install requests
pip install beautifulsoup4
```
### Performing a Basic Web Scrap

Here's a step-by-step guide to performing a basic web scrape:

1.  **Send an HTTP Request:** The first step in web scraping is to access the target website. We use the `requests.get()` method to make a GET request to the website.

```py
import requests
URL = 'https://www.example.com'
page = requests.get(URL)
```
2.  **Parse the Content:** After fetching the webpage content, we need a way to parse and extract the information we need. This is where `BeautifulSoup` comes into play.

```py
from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')
```
3.  **Extract Data:** Once you've created a `BeautifulSoup` object, you can find specific data by navigating through the parse tree. You can search for data using tag names, IDs, classes, and much more.
```py
# Find the first element with the 'class' attribute set to 'example'
example_element = soup.find(class_='example')

# Find all instances of a tag
for element in soup.find_all('a'):
    print(element.get('href'))
```
4.  **Output the Data:** After extracting the desired data, you might want to save it in a file or database for further processing or analysis.
```py
with open('output.txt', 'w') as file:
    file.write(str(example_element)) 
```
### Limitations

While `requests` and `BeautifulSoup` are fantastic tools, they do have limitations:

-   **JavaScript-heavy websites:** These libraries only fetch the HTML content, not waiting for JavaScript to execute. If the website relies on JavaScript to render content, then the HTML returned by `requests` might not contain the desired data.
    
-   **Complex web spiders:** For more complicated web scraping tasks where you need to maintain sessions, handle cookies, or crawl through website pagination, tools like Scrapy would be more suitable.
    
-   **Non-HTML data:** If you need to extract data from non-HTML/XML sources, or deal with data provided via APIs, you might need different tools or libraries.
    

Despite these limitations, mastering `requests` and `BeautifulSoup` is a valuable skill and can cover many basic web scraping needs.

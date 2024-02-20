# Web Scraping with Python: A Learning Guide

This repository provides educational material for learning web scraping using Python. It starts with the basics using `requests` and `BeautifulSoup` and then progresses to more advanced techniques with `Scrapy`.

## Table of Contents
1. [Introduction to Web Scraping](./docs/introduction.md)
2. [Basic Web Scraping with requests and BeautifulSoup](./docs/basic-web-scraping.md)
3. [Setting Up the Environment](./docs/setting-up-environment.md)
4. [Introduction to Scrapy](./docs/introduction-to-scrapy.md)
5. [Advanced Scrapy Techniques](./docs/advanced-scrapy-techniques.md)
6. [Handling JavaScript-Heavy Sites with Selenium](./docs/javascript-heavy-sites-selenium.md)
7. [Responsible Web Scraping: Best Practices and Ethics](./docs/responsible-web-scraping.md)
8. [Challenges and Solutions in Web Scraping](./docs/challenges-and-solutions.md)
9. [Practical Projects for Skill Application](./docs/practical-projects.md)
10. [Handling Data Post-Scraping](./docs/data-post-scraping.md)
11. [Sample Project: Scraping Patek.com](./projects/patek-scraping/README.md)
12. [Sample Project: Scraping Blancpain.com](./projects/blancpain-scraping/README.md)

## Prerequisites
- Basic knowledge of Python
- Python environment set up on your local machine

## Sample Projects

Practical application enhances learning. That's why we've provided sample projects that offer a hands-on approach to utilizing the concepts and techniques discussed in this tutorial. These projects demonstrate the use of popular Python libraries for web scraping: `BeautifulSoup`, `Scrapy`, and `Selenium`.

### 1. [Scraping Patek.com with Scrapy](./projects/patek-scraping/README.md)

This project showcases the power and flexibility of `Scrapy`, a comprehensive web scraping framework in Python. We've targeted Patek.com for this task, extracting detailed information about various watch models. You'll find everything you need to understand, run, and learn from this real-world example in the project's directory, including the script, sample output data, and a detailed walkthrough of the code.

### 2. [Scraping Blancpain.com with BeautifulSoup and Selenium](./projects/blancpain-scraping/README.md)

Our second project takes a different approach, using `BeautifulSoup` and `Selenium` to scrape data from Blancpain's website. While `BeautifulSoup` is perfect for simpler scraping tasks, combining it with `Selenium` allows handling JavaScript-heavy websites. This project will walk you through a practical example of how to use `BeautifulSoup` and `Selenium` for web scraping. The project's folder contains the script, sample data, and an extensive guide to understanding each step of the process.

### 3. [Scraping farfetch.com with Scrapy](./projects/farfetch-scraping/README.md)

This project, similar to Patek.com, also uses `Scrapy` to web crawl farfetch.com. We extract various fields that our client has requested. In this file, you will learn how to set up the environment, and successfully scrape and save the data to a csv file.

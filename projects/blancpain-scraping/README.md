
# Blancpain Watches Data Scraping

This project focuses on scraping detailed watch information from the official Blancpain website. Our primary goal is to extract specific data points about the watches to compile a comprehensive catalog for our client. The process involves data extraction, cleaning, and supplementation from alternative sources when necessary.

## Fields Extracted

We aim to extract the following data points for each watch listed on the Blancpain website:

-   Type
-   Brand
-   Parent Model
-   Specific Model
-   Collection
-   Name
-   Style
-   Reference Number
-   Description
-   Case Material
-   Diameter
-   Between Lugs
-   Lug to Lug
-   Thickness
-   Bezel Material
-   Bezel Color
-   Crystal
-   Water Resistance
-   Dial Color
-   Numerals
-   Bracelet Type
-   Bracelet Material
-   Bracelet Color
-   Clasp Type
-   Clasp Material
-   Movement
-   Caliber
-   Power Reserve
-   Frequency
-   Jewels
-   Features

## Prerequisites

Before setting up and running this script, ensure you have the following prerequisites installed and configured:

### Python 3

Python 3 should be installed on your system. If it's not, download and install it from the [official Python website](https://www.python.org/downloads/).

### pip

pip, the Python package installer, is usually installed with Python by default.

### Virtual Environment (recommended)

We recommend creating a virtual environment to isolate the project dependencies. You can set this up using:

`python -m venv myenv` 

To activate the virtual environment:

-   On Unix-based systems, use:
    
    `source myenv/bin/activate` 
    
-   On Windows, use:
    
    `myenv\Scripts\activate` 
    

### Chromedriver

Chromedriver is essential for Selenium to interact with the Chrome browser. Set up Chromedriver by following these steps:

1.  **Download Chromedriver:** Ensure the Chromedriver version is compatible with your Chrome browser. Download it from the [Chromedriver download page](https://googlechromelabs.github.io/chrome-for-testing/#stable).
    
2.  **Extract and Set Path:** After downloading, extract 'chromedriver.exe' to a known location. You may want to place it in the script directory or a location included in your system's PATH variable.
    
3.  **Set Executable Path in Script:** Update the `executable_path` in your script to the location of 'chromedriver.exe'. For example:
    
    `from selenium import webdriver
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')` 
    

## Output

The extracted data is compiled into a structured JSON file, making it easy to integrate into applications, databases, or websites.

## Data Cleaning and Enrichment

Post-extraction, the data undergoes thorough cleaning, including:

-   Filling in missing information from reliable alternative sources.
-   Standardizing values for consistency across the dataset.

## Usage

This section outlines the steps to set up and run the Blancpain data scraping project. These instructions allow you to replicate the scraping process, gather the watch data, and save it in a structured JSON format.

### Setting Up the Project

1.  **Clone the Repository:** Clone the repository to your local machine with this command:
    
    `git clone https://github.com/klailatimad/web-scraping-tutorial.git` 
    
2.  **Install Additional Dependencies:** This project uses Selenium, among other libraries. Install them within your virtual environment:
        
    `pip install selenium beautifulsoup4 requests lxml` 
    
3.  **Navigate to the Project Directory:** Change your directory to the `blancpain-scraping` folder in the cloned repository:
        
    `cd web-scraping-tutorial/projects/blancpain-scraping` 
    
4.  **Virtual Environment:** If you haven't already, set up and activate a virtual environment (see Prerequisites).
    

### Configuring the Project

After the initial setup, configure the specific components of the project. These include the scraping script, data processing logic, and output formatting.

1.  **Scraping Script:** Place `blancpain.py` in your project's main directory.
2.  **Data Processing:** Set up data processing or cleaning scripts to run post-scraping.
3.  **Output Formatting:** Set up the necessary utilities to format the data into a JSON file.

### Running the Scraper

With everything configured, you can run the scraping script through Python.

1.  **Navigate to the Project's Root Directory:**
       
    `cd path/to/blancpain-scraping` 
    
2.  **Run the Script:**
        
    `python blancpain.py` 
    

## Troubleshooting

-   **Chromedriver Compatibility:** If you experience compatibility issues between Chromedriver and Chrome, ensure both are updated and compatible.
-   **Permission Issues:** If there are permission errors, make sure 'chromedriver.exe' is executable and your script has the necessary permissions.

## Important Notes

-   This script is designed for educational purposes. Please comply with Blancpain's terms of service and privacy policy.
-   While we strive for data accuracy, it's not guaranteed, particularly from secondary sources. We strongly recommend independent data verification.
-   Respect the `robots.txt` of the websites you scrape and avoid overloading their servers.

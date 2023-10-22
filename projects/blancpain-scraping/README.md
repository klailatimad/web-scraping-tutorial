

# Blancpain Watches Data Scraping

This project demonstrates a practical application of web scraping, focusing on extracting detailed watch information from Blancpain's official website. We aim to compile a comprehensive catalog for our client, involving data extraction, cleaning, and supplementation from alternative sources when necessary.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Fields Extracted](#fields-extracted)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Setting Up the Project](./setting-up-the-project)
6. [Running the Script](#running-the-script)
7. [Data Storage](#data-storage)
8. [Data Cleaning and Enrichment](./docs/data-cleaning.md)
9. [Script Walkthrough](#script-walkthrough)
10. [Challenges and Solutions](#challenges-and-solutions)
11. [Troubleshooting](#troubleshooting)
12. [Important Notes](#important-notes)
13. [Learning Points](#learning-points)

## Project Overview
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
    
## Installation
### Chromedriver

Chromedriver is essential for Selenium to interact with the Chrome browser. Set up Chromedriver by following these steps:

1.  **Download Chromedriver:** Ensure the Chromedriver version is compatible with your Chrome browser. Download it from the [Chromedriver download page](https://googlechromelabs.github.io/chrome-for-testing/#stable).
    
2.  **Extract and Set Path:** After downloading, extract 'chromedriver.exe' to a known location. You may want to place it in the script directory or a location included in your system's PATH variable.
    
3.  **Set Executable Path in Script:** Update the `executable_path` in your script to the location of 'chromedriver.exe'. For example:
    
    `from selenium import webdriver
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')` 

## Setting up the Project

1.  **Clone the Repository:** Clone the repository to your local machine with this command:
    
    `git clone https://github.com/klailatimad/web-scraping-tutorial.git` 
    
2.  **Install Additional Dependencies:** This project uses Selenium, among other libraries. Install them within your virtual environment:
        
    `pip install selenium beautifulsoup4 requests lxml` 
    
3.  **Navigate to the Project Directory:** Change your directory to the `blancpain-scraping` folder in the cloned repository:
        
    `cd web-scraping-tutorial/projects/blancpain-scraping` 
    
4.  **Virtual Environment:** If you haven't already, set up and activate a virtual environment (see Prerequisites).
    

## Running the Script
This section provides detailed instructions on how to execute the scraping script once everything has been set up.

1. **Navigate to the Project's Root Directory:**
   
   Open a terminal and change your working directory to the project's root folder: 
	```
	cd path/to/blancpain-scraping
	```
2. **Execute the Script:**

	Run the script using the following command:
	```
	python blancpain.py
	```
	This command initiates the scraping process. Data extracted from the Blancpain website will be saved in a designated file (e.g., `output.json`) within the project's directory.

3.  **Monitoring the Process:** While the script is running, it logs significant events or milestones, such as completion of data extraction from a page or encountering an error. Keep an eye on these logs to understand the progress and identify any potential issues that might need attention.
    
4.  **Script Completion:** The script will notify you upon successful completion, or if it terminates due to an error. In the case of an unexpected termination, refer to the logs for more information and proceed to the troubleshooting section.

## Data Storage

The extracted data is stored in a JSON file for ease of use and compatibility. JSON format ensures the data structure  is both human-readable and easily parsed by various applications. 
- **File Name:** The default file name is `output.json`. However, you can modify the script to specify a different file name or save location. 
- **Data Format:** The data is saved in a structured JSON format, with  each watch entry constituting a JSON object  with  key-value pairs corresponding to the fields extracted.
- **Data Integrity:** The script includes measures to preserve data integrity, ensuring all extracted data is accurately saved without loss or corruption. In the event of an interruption, the script can resume from where it left off, preventing data loss.

## Script Walkthrough

The script `blancpain.py` is the core of this project. Here's a brief overview of its structure and functionality:  
1. **Imports  and Dependencies:** The script starts by importing necessary Python libraries such as `selenium`, `json`, and `time`. 
2.  **Main Function:** The `main()` function initiates the webdriver, opens the Blancpain website, and calls other functions to perform the scraping. 
3. **Data Extraction:** Various functions are defined to extract different data points like model, price, specifications, etc. These functions navigate the DOM structure  of the webpage to retrieve and store data in a Python dictionary. 
4. **Error Handling and Logging:** The script includes error handling to manage common exceptions that may occur during the scraping process, ensuring the script continues running. Errors and status updates are logged for troubleshooting. 
5. **Data Output:** After scraping is completed, the data dictionary is written to a JSON file in the local directory using the `json` library.
6. **Optimizations:** The script includes various optimizations to enhance efficiency, such as reusing the same browser session, minimizing unnecessary loads, and efficient querying. This ensures the data extraction process is not only accurate but also time-efficient.

## Challenges and Solutions
During the development of this project, we faced several challenges, especially related to website structure changes and data consistency. Here's how we tackled them: 
- **Dynamic Website Content:** Blancpain's website uses JavaScript to dynamically load content. We used Selenium to automate the browser, allowing us to interact with the JavaScript elements effectively. 
- **Data Consistency:** Some watches had missing or inconsistent information. We implemented additional logic to validate and, if necessary, standardize the data before saving it to our output file. 
- **Website Structure Changes:** The website underwent occasional design updates, affecting our script's functionality. We adopted a modular design for our scraping functions, making it easier to update specific data extraction points without overhauling the entire script.

## Troubleshooting
-   **Chromedriver Compatibility:** If you experience compatibility issues between Chromedriver and Chrome, ensure both are updated and compatible.
-   **Permission Issues:** If there are permission errors, make sure 'chromedriver.exe' is executable and your script has the necessary permissions.
- **Unexpected Script Termination:** If the script ends unexpectedly, refer to the log files to identify the last action performed. Issues could range from a lost internet connection to changes in the website’s DOM structure.
    
-   **Incomplete Data:** In cases where the data seems incomplete or malformed, verify the website's structure as it might have been updated after the script was written. Adjustments in the script may be required to adapt to the new structure.

## Important Notes

- This script is designed for educational purposes. Please comply with Blancpain's terms of service and respect their data ownership rights. Unauthorized data scraping can be legally contentious and is not condoned. 
- Data accuracy is reliant on the source website. Any missing or incorrect information should be verified independently, especially if the data will inform significant decisions or projects. 
- Be mindful of the `robots.txt` file of websites, and  do  not overload servers with frequent requests. Implement adequate delays between your requests, respecting the website's access guidelines.
-   **Rate Limiting:** Be aware of the potential for rate limiting by the server. This script does not include specific rate-limiting handling, and excessive requests in a short period might lead to your IP being temporarily blocked by the website. 
-   **Maintenance:** This script may require periodic maintenance to adapt to potential changes in the Blancpain website structure, technologies used, or content displayed. Regular testing and adaptation are key to ensuring ongoing functionality.

## Learning Points

Through this project, we gained valuable insights into various aspects of web scraping, data cleaning, and automation. Key takeaways include: 
- **Effective Web Scraping:** We learned to navigate and extract data from dynamic web pages using Selenium, handling elements that aren't immediately accessible with static scraping methods. 
- **Data Handling:** Cleaning and standardizing the extracted data was crucial to ensure consistency and reliability, emphasizing the need for robust post-processing methods.
- **Adaptability:** Regular changes in the website's structure necessitated a flexible script design, underscoring the importance of adaptability in web scraping endeavors. 
- **Ethical Considerations:** This project reinforced the significance of ethical considerations when scraping data, highlighting the necessity to respect website terms and user agreements.

# Patek Philippe Watches Data Scraping

This project focuses on scraping detailed watch information from the official Patek Philippe website. The client required specific fields related to the watches to be extracted, cleaned, and, where data was missing, supplemented from alternative sources like Chrono24 and Watchbase.

## Fields Extracted

The following fields were extracted for each watch listed on Patek.com:

- Type
- Brand
- Parent Model
- Specific Model
- Collection
- Name
- Style
- Reference Number
- Description
- Case Material
- Diameter
- Between Lugs
- Lug to Lug
- Thickness
- Bezel Material
- Bezel Color
- Crystal
- Water Resistance
- Dial Color
- Numerals
- Bracelet Type
- Bracelet Material
- Bracelet Color
- Clasp Type
- Clasp Material
- Movement
- Caliber
- Power Reserve
- Frequency
- Jewels
- Features

## Output

The data was compiled into a JSON file, ensuring a structured format that can easily be integrated into various applications, stored in a database, or loaded into their website.

## Data Cleaning and Enrichment

Post-scraping, the data underwent a cleaning process which included:

- Filling missing data by fetching required information from alternative sources such as Chrono24 and Watchbase.
- Standardizing values through defined taxonomies.

## Usage

This section outlines the steps necessary to set up and run the Patek Philippe data scraping project. By following these instructions, you'll be able to replicate the scraping process, collect the specified watch data, and save it in a structured JSON format.

### Setting Up the Project

1.  **Clone the Repository:** Start by cloning the repository to your local machine. You can do this by running the following command in your terminal or command prompt:
    
	```sh
	git clone https://github.com/your-repo.git 
	```    
2.  **Navigate to the Project Directory:** Change your current directory to the `patek-scraping` directory within the cloned repository:
    
	```sh
	cd path/to/web-scraping-tutorial/projects/patek-scraping 
	```
3.  **Install Scrapy:** If you haven't installed Scrapy yet, you can do so by running:
    ```sh
    pip install scrapy 
    ```
    This command installs Scrapy and all its dependencies.
    
4.  **Create a New Scrapy Project:** Use the Scrapy command line tool to create a new project named `patek`:
    
    ```sh
    scrapy startproject patek 
    ```
    This command creates a new folder named `patek` with the basic structure of a Scrapy project.
    

### Configuring the Project

After setting up the base project, you'll need to configure the specific components responsible for the scraping logic, data extraction, and processing. These components are provided in the repository and need to be properly placed within your Scrapy project.

1.  **Spider Script:**
    
    -   Copy the `patek.py` file from the repository into the `patek/spiders` directory of your newly created Scrapy project.
2.  **Item Definitions:**
    
    -   Replace the content of the `items.py` file in your Scrapy project with the content from `projects/patek-scraping/project_folder/items.py`.
3.  **Middlewares:**
    
    -   Update the `middlewares.py` file in your Scrapy project with the content from `projects/patek-scraping/project_folder/middlewares.py`.
4.  **Item Pipelines:**
    
    -   Replace the content of the `pipelines.py` file in your Scrapy project with the content from `projects/patek-scraping/project_folder/pipelines.py`.
5.  **Settings:**
    
    -   Update the `settings.py` file in your Scrapy project with the content from `projects/patek-scraping/project_folder/settings.py`.

### Running the Spider

With the project set up and all files in place, you're ready to start the scraping process. You have two options: running the spider directly through Scrapy or using a provided shell script that logs the output and saves the data with a timestamp.

#### Option 1: Run Directly with Scrapy

1.  **Navigate to the Scrapy Project's Root Directory:**
    ```sh
    cd path/to/patek 
    ```
2.  **Run the Spider:** Execute your spider using the following command:
    
    ```sh
	scrapy crawl patek_spider
	```
    
    Make sure to replace `patek_spider` with the actual name defined in your `patek.py` spider script.
    

#### Option 2: Use the Provided Shell Script

An alternative method is to use the `run_patek_spider.sh` script, which not only runs the spider but also generates a unique timestamp for each run, saves the scraped data to a JSON file, and logs the output to a log file.

1.  **Navigate to the Directory Containing the Script:**
    

      ```sh  
    cd path/to/script 
    ```
2.  **Make the Script Executable:** If the script is not already executable, make it so with the following command:
    
	```sh
	chmod +x run_patek_spider.sh
	 ```   
3.  **Run the Script:** Now, you can run the script with:
    
    ```sh
    ./run_patek_spider.sh 
	```    
    This command executes the spider, and the results will be saved in a file named `patek_<timestamp>.json`, and the logs will be written to `patek_<timestamp>.log`, where `<timestamp>` is the current date and time.
    

## Important Notes

-   This script was created for educational purposes. Be aware of Patek Philippe's terms of service before you attempt to scrape their site.
-   The accuracy of data filled from secondary sources can't be guaranteed. It's essential to verify the supplemental data independently.
-   Remember to respect the robots.txt file of the websites from which you are scraping data, and do not overload their servers by making too many requests in a short period.



# Blancpain Watches Data Scraping

This project is dedicated to scraping detailed watch information from the official Blancpain website. The primary goal is to extract specific data points related to the watches, which will be used to build a comprehensive catalog for our client. This involves cleaning the data and, where necessary, supplementing missing information from alternative sources.

## Fields Extracted

The following fields are targeted for extraction for each watch listed on Blancpain's website:

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

The data is compiled into a structured JSON file, making it straightforward to integrate into various applications, store in databases, or use on websites.

## Data Cleaning and Enrichment

After the extraction process, the data undergoes a comprehensive cleaning process. This involves:

- Retrieving necessary information from alternative reliable sources when data is missing.
- Standardizing values to maintain consistency across the dataset.

## Usage

This section provides a step-by-step guide on setting up and running the Blancpain data scraping project. Follow these instructions to replicate the scraping process, obtain the specified watch data, and save it in a structured JSON format.

### Setting Up the Project

1. **Clone the Repository:** Start by cloning the main repository to your local machine using the following command in your terminal or command prompt. This will download the entire repository, including the `blancpain-scraping` project:
    ```sh
    git clone https://github.com/klailatimad/web-scraping-tutorial.git
    ```
2. **Navigate to the Project Directory:** After cloning, change your current directory to the `blancpain-scraping` directory within the `web-scraping-tutorial` repository:
    ```sh
    cd web-scraping-tutorial/projects/blancpain-scraping
    ```
3. **Setting Up a Virtual Environment:** It's recommended to create a virtual environment for your project to manage dependencies. You can set up a virtual environment using the following commands:
	  ##### On Unix-based systems, use:
    ```sh
     source myenv/bin/activate
    ```
    ##### On Windows, use:
    ```sh
     myenv\Scripts\activate
    ```
5. **Install BeautifulSoup:** If you haven't already installed BeautifulSoup, do so within your virtual environment:
    ```sh
    pip install beautifulsoup4
    ```
    This command will install BeautifulSoup4 along with its dependencies.

6. **Other Dependencies:** Depending on your project's requirements, you may need to install additional packages, such as `requests` for HTTP requests or `lxml` for parsing.
    ```sh
    pip install requests lxml
    ```

### Configuring the Project

After setting up the project's base, you need to configure the specific components, including the scraping script, data processing logic, and output formatting. These components are included in the repository and should be appropriately configured within your project.

1. **Scraping Script:**
    - Place the `blancpain.py` file from the repository into your project's main directory.
2. **Data Processing:**
    - Ensure any data processing or cleaning scripts are properly set up and ready to be executed after the scraping script runs.
3. **Output Formatting:**
    - Configure the script or additional utility to format the scraped data into a JSON file.

### Running the Scraper

With the project configured, you're ready to execute the scraping script. This can be done directly through Python.

1. **Navigate to the Project's Root Directory:**
    ```sh
    cd path/to/blancpain-scraping
    ```
2. **Run the Script:** Execute your script using the following command:
    ```sh
    python blancpain.py
    ```

## Important Notes

- This script is for educational purposes. Ensure you understand and respect Blancpain's terms of service and privacy policy before scraping their site.
- Data accuracy, especially from secondary sources, cannot be fully guaranteed. Independent verification of the extracted data is strongly recommended.
- Always respect the `robots.txt` file of the websites you scrape and avoid placing excessive load on the site's servers.

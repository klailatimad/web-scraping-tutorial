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

The data was compiled into a JSON file, ensuring a structured format that can easily be integrated into various applications or used for data analysis purposes.

## Data Cleaning and Enrichment

Post-scraping, the data underwent a cleaning process which included:

- Standardizing values through defined taxonomies.
- Filling missing data by fetching required information from alternative sources such as Chrono24 and Watchbase.

## Usage

Describe here the steps a user should take to replicate your scraping project. This can include how to set up their environment, any packages they need to install, how to run your script, and where they can expect the output data to be saved.
```
TO BE EDITED
```
```sh
# Example:
# Clone the repository
git clone https://github.com/your-repo.git

# Navigate to the patek-scraping directory
cd path/to/patek-scraping

# Install dependencies
pip install -r requirements.txt

# Run the script
python script.py
```

## Important Notes

-   This script was created for educational purposes. Be aware of Patek Philippe's terms of service before you attempt to scrape their site.
-   The accuracy of data filled from secondary sources can't be guaranteed. It's essential to verify the supplemental data independently.

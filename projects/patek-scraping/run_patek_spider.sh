#!/bin/bash

# Generate a timestamp
timestamp=$(date +"%Y%m%d%H%M%S")

# Write log to file
scrapy crawl patek -o patek_${timestamp}.json -s LOG_FILE=patek_${timestamp}.log

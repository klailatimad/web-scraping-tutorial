# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
import os
import hashlib


# class PatekPipeline:
#     def process_item(self, item, spider):
#         return item
    

class CustomImagesPipeline(ImagesPipeline):
    # No need to implement this method, as we handle image URL extraction in the spider itself.
    def get_media_requests(self, item, info):
        print("Inside get_media_requests method")
        pass

    def file_path(self, request, response=None, info=None, *, item=None):
        print("Inside file_path method")
        
        # Extract the model name from the item
        model_name = item['nickname']

        # Generate a unique file name based on the model name
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        file_extension = os.path.splitext(request.url)[1]

        # Extract the part of the file name until the first underscore
        original_file_name = f'{model_name}_{image_guid}{file_extension}'
        new_file_name = original_file_name.split('_')[0]

        # Construct the file path by joining the model name and the file name
        folder_name = info.spider.name  # Use the spider name as the folder name
        file_path = os.path.join('/home/imad/Desktop/web_scraping/sandbox/patek/patek/spiders/patek_images', f'{new_file_name}{file_extension}')

        return file_path

    def item_completed(self, results, item, info):
        print("Inside item_completed method")
        return item

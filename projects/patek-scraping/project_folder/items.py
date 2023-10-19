# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PatekItem(scrapy.Item):
    brand = scrapy.Field()
    style = scrapy.Field()
    year_introduced = scrapy.Field()
    case_finish = scrapy.Field()
    caseback = scrapy.Field()
    bezel_material = scrapy.Field()
    bezel_color = scrapy.Field()
    numerals = scrapy.Field()
    bracelet_color = scrapy.Field()
    movement = scrapy.Field()
    frequency = scrapy.Field()
    jewels = scrapy.Field()
    watch_url = scrapy.Field()
    parent_model = scrapy.Field()
    specific_model = scrapy.Field()
    marketing_name =  scrapy.Field()
    nickname = scrapy.Field()
    reference_number = scrapy.Field()
    description = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    case_material = scrapy.Field()
    diameter = scrapy.Field()
    between_lugs = scrapy.Field()
    case_thickness = scrapy.Field()
    lug_to_lug = scrapy.Field()
    weight = scrapy.Field()
    water_resistance = scrapy.Field()
    crystal = scrapy.Field()
    bracelet_material = scrapy.Field()
    clasp_type = scrapy.Field()
    dial_color = scrapy.Field()
    power_reserve = scrapy.Field()
    battery_life = scrapy.Field()
    caliber = scrapy.Field()
    features = scrapy.Field()
    image_url = scrapy.Field()
    images = scrapy.Field()
    marketing_name = scrapy.Field()
    weight = scrapy.Field()
    features = scrapy.Field()
    listing_title = scrapy.Field()
    sku = scrapy.Field()
    made_in = scrapy.Field()
    case_shape = scrapy.Field()
    type = scrapy.Field()
    short_description = scrapy.Field()

    pass

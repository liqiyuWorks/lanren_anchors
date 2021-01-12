# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LanrenAnchorsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    anchor_name = scrapy.Field()
    attention_nums = scrapy.Field()
    anchor_addr = scrapy.Field()
    anchor_avatar = scrapy.Field()
    follower_nums = scrapy.Field()
    program_nums = scrapy.Field()

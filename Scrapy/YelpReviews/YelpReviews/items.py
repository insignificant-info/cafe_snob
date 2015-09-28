# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpreviewsItem(scrapy.Item):
    biz_name = scrapy.Field()
    biz_id = scrapy.Field()
    biz_hood = scrapy.Field()
    url = scrapy.Field()

    reviewer_name = scrapy.Field()
    reviewer_id = scrapy.Field()

    reviewerLoc = scrapy.Field()
    review_rating = scrapy.Field()
    review_date = scrapy.Field()
    review_text = scrapy.Field()
    review_count = scrapy.Field()

    rating = scrapy.Field()
    price_rating = scrapy.Field()
    review_count = scrapy.Field()
    attributes = scrapy.Field()


    pass

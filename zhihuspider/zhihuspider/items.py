# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = scrapy.Field()
    url_token = scrapy.Field()

    # name名字，locations居住地，educations教育背景，employment职业经历，
    name = scrapy.Field()
    locations = scrapy.Field()
    educations = scrapy.Field()
    employments = scrapy.Field()

    headline = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    badge = scrapy.Field()
    avatar_url = scrapy.Field()

    answer_count = scrapy.Field()
    question_count = scrapy.Field()
    follower_count = scrapy.Field()
    following_count = scrapy.Field()
    articles_count = scrapy.Field()



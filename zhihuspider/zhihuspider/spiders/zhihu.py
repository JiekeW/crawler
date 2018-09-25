# -*- coding: utf-8 -*-
import scrapy
import json

from zhihuspider.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = 'excited-vczh'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message%2Cquestion_count%2Cfollowing_count%2Cis_blocking%2Cdescription%2Clocations%2Ceducations%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'

    # 关注列表
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'

    # 粉丝列表
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'


    def start_requests(self):
        yield scrapy.Request(self.user_url.format(user=self.start_user,include=self.user_query), callback=self.parse_user)
        yield scrapy.Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        yield scrapy.Request(self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20),callback=self.parse_followers)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

        yield scrapy.Request(self.follows_url.format(user=result.get('url_token'), include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        yield scrapy.Request(self.followers_url.format(user=result.get('url_token'), include=self.followers_query, offset=0, limit=20),callback=self.parse_followers)

    def parse_follows(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'padding' in results.keys() and results.get('padding').get('is_end') == 'false':
            next_page = results.get('padding').get('next')
            yield scrapy.Request(next_page, callback=self.parse_follows)

    def parse_followers(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'padding' in results.keys() and results.get('padding').get('is_end') == 'false':
            next_page = results.get('padding').get('next')
            yield scrapy.Request(next_page, callback=self.parse_followers)
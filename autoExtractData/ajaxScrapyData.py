'''
使用Scrapy爬取Ajax数据，直接定位到数据API
'''

import scrapy
from scrapy.crawler import CrawlerProcess
import json

class AjaxNewsSpider(scrapy.Spider):
    name = 'ajax_courses'
    # 直接定位到数据API（通过浏览器开发者工具分析得到）
    start_urls = ['']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'news_data.json',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    }

    def parse(self, response):
        data = json.loads(response.text)
        # 处理API返回的数据
        for item in data['infos']:
            yield {
                'title': item['title'],
                'description': item['intro'],
                'articleCount': item['article']['count'],
                'price': item['price'],
                'learnedCount': item['article']['total_length'],
            }
        # 检查是否有更多数据
        if data['has_more']:
            next_page = data['next_page']
            yield scrapy.Request(
                url=f"https://API",
                callback=self.parse
            )

# 运行爬虫
process = CrawlerProcess()
process.crawl(AjaxNewsSpider)
process.start()

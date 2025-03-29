'''
 网页抓取：自动从网站提取数据
'''

import scrapy
from scrapy.crawler import CrawlerProcess
import json

class ScrollNewsSpider(scrapy.Spider):
    name = 'scroll_news'
    start_urls = ['']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0',
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'news_data.csv',
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_DELAY': 2,  # 增加延迟避免被封
    }

    def __init__(self, *args, **kwargs):
        super(ScrollNewsSpider, self).__init__(*args, **kwargs)
        self.scroll_count = 0
        self.max_scrolls = 10  # 最大滚动次数

    def parse(self, response):
        # 提取当前页面的新闻数据
        for article in response.css('.course-detail'):
            yield {
                'title': article.css('.course-title').get().strip(),
                'learnedNumber': article.css('.course-num').get(),
                'price': article.css('.course-price').get()
            }

    #     # 模拟滚动加载更多数据
    #     if self.scroll_count < self.max_scrolls:
    #         self.scroll_count += 1
    #
    #         # 构造滚动加载的API请求（需要根据实际网站调整）
    #         scroll_url = self.get_scroll_url(response)
    #         if scroll_url:
    #             yield scrapy.Request(
    #                 url=scroll_url,
    #                 callback=self.parse,
    #                 headers={'X-Requested-With': 'XMLHttpRequest'}
    #             )
    #
    # def get_scroll_url(self, response):
    #     """从页面中提取滚动加载的API URL"""
    #     script_data = response.xpath('//script[contains(., "loadMore")]/text()').get()
    #     if script_data and "apiUrl" in script_data:
    #         # 这里需要根据实际JavaScript代码提取URL
    #         return "https://time.geekbang.org/serv/v3/product/infos"

# 运行爬虫
process = CrawlerProcess()
process.crawl(ScrollNewsSpider)
process.start()
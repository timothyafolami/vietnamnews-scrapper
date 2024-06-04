from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from datetime import datetime

class CrawlingVietnam(CrawlSpider):
    name = 'vietnam_crawling'
    allowed_domains = ['vietnamnews.vn']
    start_urls = ['https://vietnamnews.vn/']
    
    # Allow all links within the domain
    rules = (
        Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        url = response.url
        
        # Extract the date from the page content
        date_str = response.xpath('//div[contains(@class, "detail__meta")]//div[contains(@class, "datetime")]/text()').get().strip()
        date = self.parse_date(date_str)
        
        if date and 2017 <= date.year <= 2024:
            title = response.xpath('//div[contains(@class, "detail__header")]//h1[contains(@class, "headline")]/text()').get().strip()
            article_content = ' '.join(response.xpath('//div[contains(@class, "detail__content")]//div[@id="abody"]//text()').getall()).strip()
            category = self.extract_category(response)
            
            yield {
                'newspaper': 'Vietnam News',
                'category': category,
                'url': url,
                'date': date.strftime('%Y-%m-%d'),
                'title': title,
                'article': article_content,
            }

    def parse_date(self, date_str):
        try:
            # Date format: 'May 13, 2024 - 14:21'
            return datetime.strptime(date_str.split(' - ')[0], '%B %d, %Y')
        except ValueError:
            return None
    
    def extract_category(self, response):
        # Extract the category from the breadcrumbs
        category = response.xpath('//div[contains(@class, "breadcrumbs")]//a[last()]/text()').get()
        return category if category else 'Unknown'

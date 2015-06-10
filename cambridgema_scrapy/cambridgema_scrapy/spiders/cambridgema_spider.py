from scrapy import Spider


class CambridgemaSpider(Spider):
    name = 'cambridge'
    allowed_domains = ['cambridgema.gov']
    start_urls = ['https://www.cambridgema.gov/propertydatabase/',]
    BASE_URL = 'https://www.cambridgema.gov'
    
    def parse(self, response):

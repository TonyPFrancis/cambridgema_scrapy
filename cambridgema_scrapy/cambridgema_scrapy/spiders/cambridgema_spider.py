from scrapy import Spider, Selector
from scrapy.http import FormRequest
import re


class CambridgemaSpider(Spider):
    name = 'cambridgema'
    allowed_domains = ['cambridgema.gov']
    start_urls = ['https://www.cambridgema.gov/propertydatabase/',]
    BASE_URL = 'https://www.cambridgema.gov'

    def parse(self, response):
        sel = Selector(response)

        __VIEWSTATE_XPATH = '//input[@id="__VIEWSTATE"]/@value'
        __VIEWSTATEGENERATOR_XPATH = '//input[@id="__VIEWSTATEGENERATOR"]/@value'
        __EVENTVALIDATION_XPATH = '//input[@id="__EVENTVALIDATION"]/@value'

        __VIEWSTATE = sel.xpath(__VIEWSTATE_XPATH).extract()
        __VIEWSTATE = __VIEWSTATE[0] if __VIEWSTATE else ''
        __VIEWSTATEGENERATOR = sel.xpath(__VIEWSTATEGENERATOR_XPATH).extract()
        __VIEWSTATEGENERATOR = __VIEWSTATEGENERATOR[0] if __VIEWSTATEGENERATOR else ''
        __EVENTVALIDATION = sel.xpath(__EVENTVALIDATION_XPATH).extract()
        __EVENTVALIDATION = __EVENTVALIDATION[0] if __EVENTVALIDATION else ''

        url = 'https://www.cambridgema.gov/propertydatabase/'
        params = {'__VIEWSTATE': __VIEWSTATE,
                  '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                  '__EVENTVALIDATION':'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',
                  'ctl00$Primary$PropertyDBSearch$txtStreetNum':'',
                  'ctl00$Primary$PropertyDBSearch$txtStreetName':'',
                  'ctl00$Primary$PropertyDBSearch$txtUnitNum':'',
                  'ctl00$Primary$PropertyDBSearch$PropertyType':'rdoPropertyType_Both',
                  'ctl00$Primary$PropertyDBSearch$txtAdvStreetNum':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvStreetName':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvUnitNum':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvLivingSqft_Low':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvLivingSqft_Hi':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvAssessedValue_Low':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvAssessedValue_High':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvSalePrice_Low':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvSalePrice_High':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvSaleDate_Low':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvSaleDate_High':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvBlockNum':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvLotNum':'',
                  'ctl00$Primary$PropertyDBSearch$txtAdvUnit':'',
                  'ctl00$Primary$PropertyDBSearch$btnAdvancedSearchSubmit':'Search'}
        yield FormRequest(url=url, formdata=params, callback=self.parse_database_list)

    def parse_database_list(self, response):
        sel = Selector(response)

        PROPERTY_DB_XPATH = '//table[@id="gvSearchResults"]/tbody/tr/td[2]/a/@href'

        property_db_links = sel.xpath(PROPERTY_DB_XPATH).extract()
        if property_db_links:
            for property_db_link in property_db_links:
                property_db_url = self.BASE_URL+property_db_link


        else:
            return

        NEXT_PAGE_XPATH = '//table[@id="gvSearchResults"]/tbody/tr/td[@colspan="7"]/table/tr/td[span]/following-sibling::td[1]/a/@href'

        next_page_link = sel.xpath(NEXT_PAGE_XPATH).extract()
        next_page_link = next_page_link[0].strip() if next_page_link else ''
        if next_page_link:
            ids = re.findall(r'\(\'(.*)?\',\'(.*)?\'', next_page_link, re.I)
            target, argument = ids[0] if ids else ('', '')

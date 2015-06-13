from scrapy import Spider, Selector
from scrapy.http import FormRequest
import re
from scrapy.shell import inspect_response
from time import sleep


class CambridgemaSpider(Spider):
    name = 'cambridgema'
    allowed_domains = ['cambridgema.gov']
    start_urls = ['https://www.cambridgema.gov/propertydatabase/',]
    BASE_URL = 'https://www.cambridgema.gov'
    PAGINATION_FIRST_INDEX = 1
    PAGINATION_LAST_INDEX = 1272
    HEADERS = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Language':'en-US,en;q=0.8',
               'Cache-Control':'max-age=0',
               'Connection':'keep-alive',
               'Host':'www.cambridgema.gov',
               'Origin':'https://www.cambridgema.gov',
               'Referer':'https://www.cambridgema.gov/propertydatabase/',
               'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'}
    COOKIES = {'_ga':'GA1.2.1291057140.1433952157',
               '_gat':'1',
               'style':'default'}

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
                  '__EVENTVALIDATION':__EVENTVALIDATION,
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
        yield FormRequest(url=url, formdata=params, callback=self.parse_database_list, dont_filter=True, headers=self.HEADERS, cookies=self.COOKIES)

    def parse_database_list(self, response):
        sel = Selector(response)

        PROPERTY_DB_XPATH = '//table[@id="gvSearchResults"]/tbody/tr/td[2]/a/@href'

        property_db_links = sel.xpath(PROPERTY_DB_XPATH).extract()
        if property_db_links:
            for property_db_link in property_db_links:
                property_db_url = self.BASE_URL+property_db_link
                print property_db_url

        else:
            return

        if self.PAGINATION_FIRST_INDEX <= self.PAGINATION_LAST_INDEX:
            __VIEWSTATE_XPATH = '//input[@id="__VIEWSTATE"]/@value'
            __VIEWSTATEGENERATOR_XPATH = '//input[@id="__VIEWSTATEGENERATOR"]/@value'
            __EVENTVALIDATION_XPATH = '//input[@id="__EVENTVALIDATION"]/@value'

            self.PAGINATION_FIRST_INDEX = self.PAGINATION_FIRST_INDEX + 1
            target, argument = 'ctl00$Primary$PropertyDBSearch$gvSearchResults', 'Page$'+str(self.PAGINATION_FIRST_INDEX)
            print "*** target, argument"
            print target, argument
            if target and argument:
                __VIEWSTATE = sel.xpath(__VIEWSTATE_XPATH).extract()
                __VIEWSTATE = __VIEWSTATE[0] if __VIEWSTATE else ''
                __VIEWSTATEGENERATOR = sel.xpath(__VIEWSTATEGENERATOR_XPATH).extract()
                __VIEWSTATEGENERATOR = __VIEWSTATEGENERATOR[0] if __VIEWSTATEGENERATOR else ''
                __EVENTVALIDATION = sel.xpath(__EVENTVALIDATION_XPATH).extract()
                __EVENTVALIDATION = __EVENTVALIDATION[0] if __EVENTVALIDATION else ''
                url = 'https://www.cambridgema.gov/propertydatabase/'
                params = {'__EVENTTARGET': target,
                          '__EVENTARGUMENT': argument,
                          '__VIEWSTATE': __VIEWSTATE,
                          '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                          '__EVENTVALIDATION': __EVENTVALIDATION}
                print params
                sleep(10)
                yield FormRequest(url=url, formdata=params, callback=self.parse_database_list, dont_filter=True, headers=self.HEADERS, cookies=self.COOKIES)


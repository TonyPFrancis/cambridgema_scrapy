from scrapy import Spider, Selector
from scrapy.http import FormRequest
import re
from scrapy.shell import inspect_response


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
        yield FormRequest(url=url, formdata=params, callback=self.get_database_list_limit)

    def get_database_list_limit(self, response):
        sel = Selector(response)

        LAST_INDEX_XPATH = '//table[@id="gvSearchResults"]/tbody/tr/td[@colspan="7"]/table/tr/td/a[text()="Last Page"]/@href'
        __VIEWSTATE_XPATH = '//input[@id="__VIEWSTATE"]/@value'
        __VIEWSTATEGENERATOR_XPATH = '//input[@id="__VIEWSTATEGENERATOR"]/@value'
        __EVENTVALIDATION_XPATH = '//input[@id="__EVENTVALIDATION"]/@value'

        last_page_link = sel.xpath(LAST_INDEX_XPATH).extract()
        last_page_link = last_page_link[0].strip() if last_page_link else ''
        if last_page_link:
            ids = re.findall(r'\(\'(.*)?\',\'(.*)?\'', last_page_link, re.I)
            target, argument = ids[0] if ids else ('', '')
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
                yield FormRequest(url=url, formdata=params, callback=self.parse_database_list)

    def parse_database_list(self, response):
        sel = Selector(response)

        PROPERTY_DB_XPATH = '//table[@id="gvSearchResults"]/tbody/tr/td[2]/a/@href'

        property_db_links = sel.xpath(PROPERTY_DB_XPATH).extract()
        print "*** property_db_links"
        print property_db_links
        if property_db_links:
            for property_db_link in property_db_links:
                property_db_url = self.BASE_URL+property_db_link
                print property_db_url

        else:
            return

        NEXT_PAGE_XPATH = '//table[@id="gvSearchResults"]/tbody/tr/td[@colspan="7"]/table/tr/td[span]/following-sibling::td[1]/a/@href'
        __VIEWSTATE_XPATH = '//input[@id="__VIEWSTATE"]/@value'
        __VIEWSTATEGENERATOR_XPATH = '//input[@id="__VIEWSTATEGENERATOR"]/@value'
        __EVENTVALIDATION_XPATH = '//input[@id="__EVENTVALIDATION"]/@value'

        next_page_link = sel.xpath(NEXT_PAGE_XPATH).extract()
        next_page_link = next_page_link[0].strip() if next_page_link else ''
        print "*** next_page_link"
        print next_page_link
        if not next_page_link:
            inspect_response(response)
        if next_page_link:
            ids = re.findall(r'\(\'(.*)?\',\'(.*)?\'', next_page_link, re.I)
            target, argument = ids[0] if ids else ('', '')
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
                yield FormRequest(url=url, formdata=params, callback=self.parse_database_list)


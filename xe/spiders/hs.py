#!/usr/bin/python
# coding=utf-8

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
import datetime

class hs(CrawlSpider):
    name = "hs"
    download_delay = 2
    allowed_domains = ["xe.gr"]

    #start_urls = ["http://www.xe.gr/property/search?Publication.age=1&System.item_type=re_residence&Transaction.type_channel=117518&page=1&per_page=50"]
    start_urls = ["http://www.xe.gr/property/search?System.item_type=re_residence&Transaction.type_channel=117518&Geo.area_id_new__hierarchy=82188&Item.type=31947"]

    rules = (Rule(LxmlLinkExtractor(allow_domains = ('xe.gr'), restrict_xpaths = ("//a[@class='white_button right']")), callback='parse_start_url', follow=True),)

    def parse_start_url(self, response):
        return self.parse_items(response)

    def parse_items(self, response):
        for sel in response.xpath("//div[contains(@class,'r_desc')]/h2/a"):
            link = "http://www.xe.gr"+sel.xpath("@href").extract_first()+"?mode=spec"
            yield Request(link, callback=self.parse2)

    def parse2(self, response):
        # Creating an empty item object
        item = {}
        # Assigning values to it's fields
        item['url'] = response.url
        region_string = response.xpath(u"//th[text()='Περιοχή:']/following-sibling::*/text()").extract_first()
        region_list = region_string.strip().split(' > ')
        item['regionA'] = region_list[0]
        try:
            item['regionB'] = region_list[1]
        except (IndexError):
            item['regionB'] = None
        try:
            item['regionC'] = region_list[2]
        except (IndexError):
            item['regionC'] = None
        try:
            item['regionD'] = region_list[3]
        except (IndexError):
             item['regionD'] = None
        item['category'] = response.xpath(u"//th[text()='Είδος:']/following-sibling::*/text()").extract_first()
        item['house_type'] = response.xpath(u"//th[text()='Τύπος Ακινήτου:']/following-sibling::*/text()").extract_first()
        price_string = response.xpath(u"//td[@class='auto_price']/span/text()").extract_first()
        try:
            item['price'] = float(price_string.strip().replace(u" €","").replace(".","").replace(",","."))
        except:
            item['price'] = None
        area_string = response.xpath(u"//th[text()='Εμβαδόν:']/following-sibling::*/text()").extract_first()
        try:
            item['area'] = float(area_string.strip().replace(".","").replace(",","."))
        except:
            item['area'] = None
        item['floor'] = response.xpath(u"//th[text()='Όροφος:']/following-sibling::*/text()").extract_first()
        construction_year_string = response.xpath(u"//th[text()='Έτος Κατασκευής:']/following-sibling::*/text()").extract_first()
        try:
            item['construction_year'] = int(construction_year_string)
        except:
            item['construction_year'] = None
        item['condition'] = response.xpath(u"//th[text()='Κατάσταση:']/following-sibling::*/text()").extract_first()
        item['condition_details'] = response.xpath(u"//th[text()='Λεπτομερής κατάσταση:']/following-sibling::*/text()").extract_first()
        try:
            item['bedrooms'] = int(response.xpath(u"//th[text()='Υπνοδωμάτια:']/following-sibling::*/text()").extract_first())
        except:
            item['bedrooms'] = None
        try:
            item['bath_wc'] = int(response.xpath(u"//th[text()='Μπάνια/ WC:']/following-sibling::*/text()").extract_first())
        except:
            item['bath_wc'] = None
        item['parking'] = response.xpath(u"//th[text()='Πάρκιν:']/following-sibling::*/text()").extract_first()
        item['parking_type'] = response.xpath(u"//th[text()='Είδος Πάρκιν:']/following-sibling::*/text()").extract_first()
        item['heating_autonomus'] = response.xpath(u"//th[text()='Αυτόνομη θέρμανση:']/following-sibling::*/text()").extract_first()
        item['natural_gas'] = response.xpath(u"//th[text()='Φυσικό αέριο:']/following-sibling::*/text()").extract_first()
        item['fireplace'] = response.xpath(u"//th[text()='Τζάκι:']/following-sibling::*/text()").extract_first()
        item['heating_cooling'] = response.xpath(u"//th[text()='Κλιματισμός:']/following-sibling::*/text()").extract_first()
        item['solar_water_heater'] = response.xpath(u"//th[text()='Ηλιακός θερμοσίφωνας:']/following-sibling::*/text()").extract_first()
        item['energy_class'] = response.xpath(u"//th[text()='Ενεργειακή Κλάση:']/following-sibling::*/text()").extract_first()
        item['awnings'] = response.xpath(u"//th[text()='Τέντες:']/following-sibling::*/text()").extract_first() #  item[''] = response.xpath(u"//th[text()='']/following-sibling::*/text()").extract_first()
        item['safety_door'] = response.xpath(u"//th[text()='Πόρτα ασφαλείας:']/following-sibling::*/text()").extract_first()
        item['pool'] = response.xpath(u"//th[text()='Πισίνα:']/following-sibling::*/text()").extract_first()
        item['no_shared_utility_bills'] = response.xpath(u"//th[text()='Χωρίς Κοινόχρηστα:']/following-sibling::*/text()").extract_first()
        item['storeroom'] = response.xpath(u"//th[text()='Με αποθήκη:']/following-sibling::*/text()").extract_first()
        item['no_elevator'] = response.xpath(u"//th[text()='Χωρίς ασανσέρ:']/following-sibling::*/text()").extract_first()
        #  Τώρα θα πάμε να πάρουμε και την ημερομηνία τελευταίας τροποποίησης.
        yield Request(response.url[:-10], callback=self.parse3, meta={'item': item})


    def parse3(self, response):
        # Retrieving the item
        item = response.meta['item']
        # Assigning more values to it's fields
        x = response.xpath("//td[@class='headItem']/text()").extract_first()
        datelist = x.split(" ")
        months = [u'Ιανουαρίου',u'Φεβρουαρίου',u'Μαρτίου',u'Απριλίου',u'Μαΐου',u'Ιουνίου',u'Ιουλίου',u'Αυγούστου',u'Σεπτεμβρίου',u'Οκτωβρίου',u'Νοεμβρίου',u'Δεκεμβρίου']
        date = datetime.date(int(datelist[3]), months.index(datelist[2])+1, int(datelist[1]))
        item['date'] = date
        try:
            item['details'] = response.xpath("//p[@class='dets']").xpath("text()").extract_first().strip()
        except:
            item['details'] = None
        yield item

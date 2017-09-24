#!/usr/bin/python
# coding=utf-8

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
import datetime


class lr(CrawlSpider):
    name = "lr"
    download_delay = 2
    allowed_domains = ["xe.gr"]

    start_urls = ["http://www.xe.gr/property/search?Publication.age=1&System.item_type=re_land&Transaction.type_channel=117541&page=1&per_page=50"]

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
        price_string = response.xpath(u"//td[@class='auto_price']/span/text()").extract_first()
        try:
            item['price'] = float(price_string.strip().replace(u" €","").replace(".","").replace(",","."))
        except:
            item['price'] = None
        item['location_name'] = response.xpath(u"//th[text()='Τοποθεσία:']/following-sibling::*/text()").extract_first()
        item['category'] = response.xpath(u"//th[text()='Είδος:']/following-sibling::*/text()").extract_first()
        area_string = response.xpath(u"//th[text()='Εμβαδόν:']/following-sibling::*/text()").extract_first()
        try:
            item['area'] = float(area_string.strip().replace(".","").replace(",","."))
        except:
            item['area'] = None
        item['city_plan'] = response.xpath(u"//th[text()='Σχέδιο Πόλης:']/following-sibling::*/text()").extract_first()
        item['structure_factor'] = response.xpath(u"//th[text()='Συντελεστής Δόμησης:']/following-sibling::*/text()").extract_first()
        item['coverage_factor'] = response.xpath(u"//th[text()='Συντελεστής Κάλυψης:']/following-sibling::*/text()").extract_first()
        facade_length_string = response.xpath(u"//th[text()='Πρόσοψη:']/following-sibling::*/text()").extract_first()
        try:
            item['facade_length'] = float(facade_length_string)
        except:
            item['facade_length'] = None
        try:
            item['facade_count'] = float(response.xpath(u"//th[text()='Αριθμός Όψεων:']/following-sibling::*/text()").extract_first())
        except:
            item['facade_count'] = None
        item['airy'] = response.xpath(u"//th[text()='Διαμπερές:']/following-sibling::*/text()").extract_first()
        item['slope'] = response.xpath(u"//th[text()='Κλίση:']/following-sibling::*/text()").extract_first()
        item['artio'] = response.xpath(u"//th[text()='Άρτιο:']/following-sibling::*/text()").extract_first()
        item['oikodomisimo'] = response.xpath(u"//th[text()='Οικοδομήσιμο:']/following-sibling::*/text()").extract_first()
        item['me_adia'] = response.xpath(u"//th[text()='Με άδεια οικοδομής:']/following-sibling::*/text()").extract_first()
        try:
            item['ktizei'] = float(response.xpath(u"//th[text()='Κτίζει:']/following-sibling::*/text()").extract_first())
        except:
            item['ktizei'] = None
        item['availability'] = response.xpath(u"//th[text()='Διαθεσιμότητα:']/following-sibling::*/text()").extract_first()
        item['availability_from'] = response.xpath(u"//th[text()='Διαθέσιμο από:']/following-sibling::*/text()").extract_first()
        item['antiparoxi'] = response.xpath(u"//th[text()='Και αντιπαροχή:']/following-sibling::*/text()").extract_first() # Δεν είμαι σίγουρος για το xpath
        item['view'] = response.xpath(u"//th[text()='Θέα:']/following-sibling::*/text()").extract_first()
        try:
            item['dist_from_sea'] = float(response.xpath(u"//th[text()='Απόσταση από Θάλασσα:']/following-sibling::*/text()").extract_first())
        except:
            item['dist_from_sea'] = None
        item['paling'] = response.xpath(u"//th[text()='Περίφραξη:']/following-sibling::*/text()").extract_first()
        item['supplies'] = response.xpath(u"//th[text()='Παροχές:']/following-sibling::*/text()").extract_first()
        item['drilling'] = response.xpath(u"//th[text()='Γεώτρηση:']/following-sibling::*/text()").extract_first()
        item['with_building'] = response.xpath(u"//th[text()='Κτίσμα:']/following-sibling::*/text()").extract_first()
        item['corner_plot'] = response.xpath(u"//th[text()='Γωνιακό:']/following-sibling::*/text()").extract_first()
        item['mesites'] = response.xpath(u"//th[text()='Μεσίτες δεκτοί:']/following-sibling::*/text()").extract_first()
        item['epaggelmatiki_xrisi'] = response.xpath(u"//th[text()='Επαγγελματική χρήση:']/following-sibling::*/text()").extract_first()
        item['dimensions'] = response.xpath(u"//th[text()='Διαστάσεις:']/following-sibling::*/text()").extract_first()
        item['contains'] = response.xpath(u"//th[text()='Περιέχει:']/following-sibling::*/text()").extract_first()
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

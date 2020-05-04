import scrapy 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from Walmart.items import WalmartItem


class WalmartSpider(CrawlSpider):
    name = 'Walmart'
    #number of items to process
    item_count = 0
    #url to work
    allowed_domain = ['https://www.walmart.ca/']

    #category url and branch
    start_url = [
        'https://www.walmart.ca/en/grocery/fruits-vegetables/N-3799'
        # 'https://www.walmart.ca/en/grocery/dairy-eggs/N-3798',
        # 'https://www.walmart.ca/en/grocery/meat-seafood/N-3793',
        # 'https://www.walmart.ca/en/grocery/pantry-food/N-3794',
        # 'https://www.walmart.ca/en/grocery/natural-organic-food/N-3992',
        # 'https://www.walmart.ca/en/grocery/frozen-food/N-3795',
        # 'https://www.walmart.ca/en/grocery/bakery/N-3796',
        # 'https://www.walmart.ca/en/grocery/deli-ready-made-meals/N-3792',
        # 'https://www.walmart.ca/en/grocery/pantry-food/chips-snacks/N-3842',
        # 'https://www.walmart.ca/en/grocery/pantry-food/cereal-breakfast/N-3830',
        # 'https://www.walmart.ca/en/grocery/drinks/N-3791',
        # 'https://www.walmart.ca/en/grocery/international-foods/N-4356',
        # 'https://www.walmart.ca/en/grocery/pantry-food/pasta-rice-beans/N-3835',
        # 'https://www.walmart.ca/en/grocery/pets/N-3797',
        # 'https://www.walmart.ca/en/grocery/household-cleaning-supplies/N-3803',
        # 'https://www.walmart.ca/en/grocery/health-beauty-pharmacy/N-3800',
        # 'https://www.walmart.ca/en/grocery/baby/N-3789',
        # 'https://www.walmart.ca/en/grocery/home-outdoor/N-8584'

        ]

    #rules and restriction
    rules  = {
        Rule(LinkExtractor(allow  = (), restrict_xpaths = ('//a[@class="page-select-list-btn"]'))),
        Rule(LinkExtractor(allow  = (), restrict_xpaths = ('//h2[@class="thumb-header"]'))
                            callback = 'parse_item', follow = False)
    }

    def parse_item(self, response):
        walmart_item = WalmartItem()

        #product information 
        walmart_item['barCodes'] = response.xpath('normalize-space(/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/section[3]/div[2]/div/div[1]/div[7]/div[2]/text())').extract()
        walmart_item['sku'] = response.xpath('normalize-space(/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/section[3]/div[2]/div/div[1]/div[6]/div[2]/text())').extract()
        walmart_item['brand'] = response.xpath('normalize-space(/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/section[3]/div[2]/div/div[1]/div[3]/div[2]/text())').extract()
        walmart_item['name'] = response.xpath('normalize-space(//h1[@class= "css-1c6krh5 e1yn5b3f7"]/text())').extract()
        walmart_item['description'] = response.xpath('normalize-space(//div[@class= "css-gur09u e1mpbtcv1"]/text())').extract()
        walmart_item['package'] = response.xpath('normalize-space(//div[@class= "css-1hxe5mn e6y1pbs0"]/text())').extract()
        walmart_item['imageUrl'] = response.xpath('normalize-space(//*[starts-with(@property, "og:image")]/@content/text())').extract()
        walmart_item['category'] = response.xpath('normalize-space(//li[@class= "css-1wco68u e16uoh2c4"]/text())').extract()
        walmart_item['productUrl'] = response.xpath('normalize-space(//*[starts-with(@property, "og:url")]/@content/text())').extract()
        walmart_item['dataJson'] = response.xpath('normalize-space(/html/body/script[1]/text())').extract()

        #branchProducts information
        walmart_item['product'] = response.xpath('')#productID 
        walmart_item['branch'] = response.xpath('') #store ID
        walmart_item['stock'] = response.xpath('normalize-space(//span[@class="css-1l7huhm e17mwry0"]/text())').extract()
        walmart_item['price'] = response.xpath('normalize-space(//span[@class="css-2vqe5n esdkp3p0"]/text())').extract_first()
        self.item_count += 1
        if self.item_count > 3:
            raise CloseSpider('item_exceeded')
        yield walmart_item    
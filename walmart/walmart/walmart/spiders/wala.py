# -*- coding: utf-8 -*-
import scrapy
import json
from io import StringIO
from json import JSONEncoder
import pickle
from scrapy.http import Response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags, remove_tags_with_content
from walmart.items import WalmartItem

class WalSpider(CrawlSpider):
    name = 'wala'
    item_count = 0
    # start_urls = [
    #     'https://www.walmart.ca/en/grocery/fruits-and-vegetables/N-3799', 
    #     'https://www.walmart.ca/en/grocery/dairy-eggs/N-3798', 
    #     'https://www.walmart.ca/en/grocery/meat-seafood/N-3793',
    #     'https://www.walmart.ca/en/grocery/pantry-food/N-3794', 
    #     'https://www.walmart.ca/en/grocery/natural-organic-food/N-3992',
    #     'https://www.walmart.ca/en/grocery/frozen-food/N-3795',
    #     'https://www.walmart.ca/en/grocery/bakery/N-3796',
    #     'https://www.walmart.ca/en/grocery/deli-ready-made-meals/N-3792',
    #     'https://www.walmart.ca/en/grocery/drinks/N-3791',
    #     'https://www.walmart.ca/en/grocery/international-foods/N-4356',
    #     'https://www.walmart.ca/en/grocery/household-supplies/N-3803', 
    #     'https://www.walmart.ca/en/grocery/health-beauty-pharmacy/N-3800', 
    #     'https://www.walmart.ca/en/grocery/baby/N-3789', 
    #     'https://www.walmart.ca/en/grocery/pets/N-3797', 
    #     'https://www.walmart.ca/en/grocery/pantry-food/chips-snacks/N-3842', 
    #     'https://www.walmart.ca/en/grocery/dairy-eggs/milk-cream/N-3851', 
    #     'https://www.walmart.ca/en/grocery/pantry-food/pasta-rice-beans/N-3835',
    #     'https://www.walmart.ca/en/grocery/frozen-food/frozen-meat-seafood/N-3827'
    # ]
  
    
    start_urls = [
        'https://www.walmart.ca/en/grocery/fruits-and-vegetables/N-3799', 
        'https://www.walmart.ca/en/grocery/dairy-eggs/N-3798', 
    ]
    def start_requests(self):
        
        url = "https://www.walmart.ca/en/grocery/N-117"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Content-Type": "application/json; charset=UTF-8",
            "Cookie": 'walmart.shippingPostalCode=P7B3Z7; defaultNearestStoreId=3124; zone=9; deliveryCatchment=3124; walmart.csrf=f88f4b5149adef8d907736a1; wmt.c=0; vtc=WlrDORHfE5eaKvhzqakNKE; userSegment=10-percent; TBV=7; rxVisitor=15887896828899FUFOLKLATMA611L568OGF85KAPCHTRC; headerType=grocery; AMCVS_C4C6370453309C960A490D44%40AdobeOrg=1; walmart.id=08ab1e32-3a4a-49fd-88ae-28218bf762bf; usrState=1; _ga=GA1.2.484015444.1588875313; s_ecid=MCMID%7C05034263762608013960105857420568304998; walmart.nearestPostalCode=P7B3Z7; walmart.locale=en; _gcl_au=1.1.779450552.1588875313; og_session_id=af0a84f8847311e3b233bc764e1107f2.173286.1588875313; og_session_id_conf=af0a84f8847311e3b233bc764e1107f2.173286.1588875313; s_visit=1; _fbp=fb.1.1588875313733.844915520; s_cc=true; __gads=ID=d10600aed34d6fd1:T=1588875312:S=ALNI_MaGYlHwled0ITkov_MQymv3gq6wyw; og_autoship=0; _pin_unauth=MWM2MWQyMDEtODFmZi00Zjg4LWFjOTYtNDIxNzRhM2VlNmM0; walmart.nearestLatLng="48.4120872,-89.2413988"; dtSa=-; dtLatC=13; rxVisitor=15887896828899FUFOLKLATMA611L568OGF85KAPCHTRC; enableHTTPS=1; dtSa=-; dtCookie=22$T4CF2FTNEMMV3A34NTKGFK21570UOEBN|5b6d58542e634882|0; AMCV_C4C6370453309C960A490D44%40AdobeOrg=-408604571%7CMCIDTS%7C18394%7CMCMID%7C05034263762608013960105857420568304998%7CMCAAMLH-1589840438%7C7%7CMCAAMB-1589840438%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589242838s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; _gid=GA1.2.899032113.1589235639; s_sq=%5B%5BB%5D%5D; previousBreakpoint=mobile; wmt.breakpoint=m; s_gnr=1589236175304-Repeat; ENV=ak-dfw-prod; bstc=eDbL1gncLdFrMOikJGxiWg; xpa=34JTv|HeXkG|LVSOt|MPTAC|MZ9tt|NOECn|NOaJP|btyTC|eP05T|gbvoH|jeBOs|lZnE7|mOlOu|oygXn|pXPz1|qvGc6|sGGbM|ssJZF|t5K4Y|xzlm3|yI7_k|yntCW|zilS-; exp-ck=34JTv2HeXkG1LVSOt1MPTACkMZ9tt1NOECn2NOaJPHbtyTC1eP05T1gbvoH1jeBOs8lZnE76mOlOuIoygXn1pXPz13qvGc62sGGbM4ssJZF7t5K4Y1xzlm33yI7_k1yntCW1zilS-3; TS01f4281b=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; TS011fb5f6=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; TS0175e29f=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; akaau_P1=1589249999~id=581b7e77ece54e0930f40fae41509094; rxvt=1589250000058|1589248012866; dtPC=22$448200046_67h1vXBTXAKEWMXNSBIGMPYXXOSAJDFBSPUIS-0; _4c_= jVNdb5swFP0rlaX1KYA%2FwJhIVZVmVbdpadeuUx%2BRazvBKgFknLIsyn%2FfNU368VZe4J57zuVe3%2BMdGirToCnJREFTQTEljE%2FQk9n2aLpDzurwekZTZHJecEVkJJZGRWnBRVSoXEcqX7LMCJ4taY4m6G%2BoVfC0EIzjNC32E6SbYw1tlnJT%2BzdahjNOc8IF0OyRJT%2FmGc8Zg7wbDoRjIuNFWnygjghQVXeg7tDG1VCy8r7rp0kyDEM8yHotnY%2BVTEyTrFyrjNsm1xEhoX%2FVagMCUsQiziD2%2FyCKGMbw3blWb5Qv%2FbYLnME8nvT6CRLaPFtlysFqXwUxFfgNrYxdVR7gnI5o5wJlLD7YRrfDqw5O%2Fw18lXESZI%2BuHXoTpPPKtWtzIgigLWwJPYyCHkJnlsa5kfXJic%2BtsvqsgoJfKO7kypTffpVz6c2qddvy3tamvHrhlw8L%2BENv%2FTj6a8UDBoYBOJxR2GCYrW6VrAMX7DVBV7Pyz%2Fev4zQ54yxN0xgsJ%2BBIWB7YN4v7u%2FLicja%2FuX7XfLturN84E%2FV9%2FX6Kx6Tvk2FtlWyklmEtCUl%2B%2FI5oTESMo5%2BzO5b0jImMCzA15oTm57PbizNyuoZpcYZZSjnLOeVYYMIKjgnORJanFEwkGE6LQpzObi%2FPyLG1xXzs%2FnNSEN07u1oZtzC%2BauEKQSy19bZtZI1ebsS7y6DDmlUt%2B94qbfon33ZofzC2KBijnLCcEjCjBzMLnuLw7Pf7%2Fw%3D%3D; _uetsid=_uetec6faf63-2714-a1a6-39d3-e374a14f0eef; xpm=1%2B1589247775%2BWlrDORHfE5eaKvhzqakNKE~%2B0; _derived_epik=dj0yJnU9SGV3OEVrcW8yWWNnSDliUWplMDc0MzJuNEdtcEVzelUmbj0tT1RPTTV6ZC1kUjZLOGZOTlBkYUNBJm09NyZ0PUFBQUFBRjY2QU1v; seqnum=5,Host: www.walmart.ca',            
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        yield scrapy.Request(url=url, method="POST", headers=headers, callback=self.parse)

    def parse(self, response):
        base_url = 'www.walmart.ca'
        url = "https://www.walmart.ca/en/grocery/fruits-vegetables/N-3799/"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Content-Type": "application/json; charset=UTF-8",
            "Cookie": 'walmart.shippingPostalCode=P7B3Z7; defaultNearestStoreId=3124; zone=9; deliveryCatchment=3124; walmart.csrf=f88f4b5149adef8d907736a1; wmt.c=0; vtc=WlrDORHfE5eaKvhzqakNKE; userSegment=10-percent; TBV=7; rxVisitor=15887896828899FUFOLKLATMA611L568OGF85KAPCHTRC; headerType=grocery; AMCVS_C4C6370453309C960A490D44%40AdobeOrg=1; walmart.id=08ab1e32-3a4a-49fd-88ae-28218bf762bf; usrState=1; _ga=GA1.2.484015444.1588875313; s_ecid=MCMID%7C05034263762608013960105857420568304998; walmart.nearestPostalCode=P7B3Z7; walmart.locale=en; _gcl_au=1.1.779450552.1588875313; og_session_id=af0a84f8847311e3b233bc764e1107f2.173286.1588875313; og_session_id_conf=af0a84f8847311e3b233bc764e1107f2.173286.1588875313; s_visit=1; _fbp=fb.1.1588875313733.844915520; s_cc=true; __gads=ID=d10600aed34d6fd1:T=1588875312:S=ALNI_MaGYlHwled0ITkov_MQymv3gq6wyw; og_autoship=0; _pin_unauth=MWM2MWQyMDEtODFmZi00Zjg4LWFjOTYtNDIxNzRhM2VlNmM0; walmart.nearestLatLng="48.4120872,-89.2413988"; dtSa=-; dtLatC=13; rxVisitor=15887896828899FUFOLKLATMA611L568OGF85KAPCHTRC; enableHTTPS=1; dtSa=-; dtCookie=22$T4CF2FTNEMMV3A34NTKGFK21570UOEBN|5b6d58542e634882|0; AMCV_C4C6370453309C960A490D44%40AdobeOrg=-408604571%7CMCIDTS%7C18394%7CMCMID%7C05034263762608013960105857420568304998%7CMCAAMLH-1589840438%7C7%7CMCAAMB-1589840438%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589242838s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; _gid=GA1.2.899032113.1589235639; s_sq=%5B%5BB%5D%5D; previousBreakpoint=mobile; wmt.breakpoint=m; s_gnr=1589236175304-Repeat; ENV=ak-dfw-prod; bstc=eDbL1gncLdFrMOikJGxiWg; xpa=34JTv|HeXkG|LVSOt|MPTAC|MZ9tt|NOECn|NOaJP|btyTC|eP05T|gbvoH|jeBOs|lZnE7|mOlOu|oygXn|pXPz1|qvGc6|sGGbM|ssJZF|t5K4Y|xzlm3|yI7_k|yntCW|zilS-; exp-ck=34JTv2HeXkG1LVSOt1MPTACkMZ9tt1NOECn2NOaJPHbtyTC1eP05T1gbvoH1jeBOs8lZnE76mOlOuIoygXn1pXPz13qvGc62sGGbM4ssJZF7t5K4Y1xzlm33yI7_k1yntCW1zilS-3; TS01f4281b=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; TS011fb5f6=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; TS0175e29f=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; akaau_P1=1589249999~id=581b7e77ece54e0930f40fae41509094; rxvt=1589250000058|1589248012866; dtPC=22$448200046_67h1vXBTXAKEWMXNSBIGMPYXXOSAJDFBSPUIS-0; _4c_= jVNdb5swFP0rlaX1KYA%2FwJhIVZVmVbdpadeuUx%2BRazvBKgFknLIsyn%2FfNU368VZe4J57zuVe3%2BMdGirToCnJREFTQTEljE%2FQk9n2aLpDzurwekZTZHJecEVkJJZGRWnBRVSoXEcqX7LMCJ4taY4m6G%2BoVfC0EIzjNC32E6SbYw1tlnJT%2BzdahjNOc8IF0OyRJT%2FmGc8Zg7wbDoRjIuNFWnygjghQVXeg7tDG1VCy8r7rp0kyDEM8yHotnY%2BVTEyTrFyrjNsm1xEhoX%2FVagMCUsQiziD2%2FyCKGMbw3blWb5Qv%2FbYLnME8nvT6CRLaPFtlysFqXwUxFfgNrYxdVR7gnI5o5wJlLD7YRrfDqw5O%2Fw18lXESZI%2BuHXoTpPPKtWtzIgigLWwJPYyCHkJnlsa5kfXJic%2BtsvqsgoJfKO7kypTffpVz6c2qddvy3tamvHrhlw8L%2BENv%2FTj6a8UDBoYBOJxR2GCYrW6VrAMX7DVBV7Pyz%2Fev4zQ54yxN0xgsJ%2BBIWB7YN4v7u%2FLicja%2FuX7XfLturN84E%2FV9%2FX6Kx6Tvk2FtlWyklmEtCUl%2B%2FI5oTESMo5%2BzO5b0jImMCzA15oTm57PbizNyuoZpcYZZSjnLOeVYYMIKjgnORJanFEwkGE6LQpzObi%2FPyLG1xXzs%2FnNSEN07u1oZtzC%2BauEKQSy19bZtZI1ebsS7y6DDmlUt%2B94qbfon33ZofzC2KBijnLCcEjCjBzMLnuLw7Pf7%2Fw%3D%3D; _uetsid=_uetec6faf63-2714-a1a6-39d3-e374a14f0eef; xpm=1%2B1589247775%2BWlrDORHfE5eaKvhzqakNKE~%2B0; _derived_epik=dj0yJnU9SGV3OEVrcW8yWWNnSDliUWplMDc0MzJuNEdtcEVzelUmbj0tT1RPTTV6ZC1kUjZLOGZOTlBkYUNBJm09NyZ0PUFBQUFBRjY2QU1v; seqnum=5,Host: www.walmart.ca',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        start_urls = response.xpath('//div[@class="media-tracking tile desktop6 tablet3 mobile2  seoTile"]/a/@href').extract()
        # print('start_urls', start_urls)
        # for newUrl in start_urls:
        #     print('si llega', newUrl)
        yield scrapy.Request(url=url, method="POST",  headers=headers, callback=self.parse_item)
        #     start_urls = base_url + url
        #     print('start_urls', start_urls)
        # for url in self.start_urls:
        #     print('url', url)

        # request = scrapy.Request(url=url, method="POST", headers=headers, callback=self.parse_item)
        # print('request', request)
        # yield request

        # if(urlsGrocery):
        #     for url in urlsGrocery:
        #         urlDepartments = base_url + url
        #         request = scrapy.Request(urlDepartments,  method="POST", callback=self.second_parse, headers=headers)
        #         yield request

    def parse_item(self, response):
        # headers = {
        #     "Accept": "application/json, text/javascript, */*; q=0.01",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        #     "Content-Type": "application/json; charset=UTF-8",
        #     "Cookie": 'walmart.shippingPostalCode=P7B3Z7; defaultNearestStoreId=3124; zone=9; deliveryCatchment=3124; walmart.csrf=f88f4b5149adef8d907736a1; wmt.c=0; vtc=WlrDORHfE5eaKvhzqakNKE; userSegment=10-percent; TBV=7; rxVisitor=15887896828899FUFOLKLATMA611L568OGF85KAPCHTRC; headerType=grocery; AMCVS_C4C6370453309C960A490D44%40AdobeOrg=1; walmart.id=08ab1e32-3a4a-49fd-88ae-28218bf762bf; usrState=1; _ga=GA1.2.484015444.1588875313; s_ecid=MCMID%7C05034263762608013960105857420568304998; walmart.nearestPostalCode=P7B3Z7; walmart.locale=en; _gcl_au=1.1.779450552.1588875313; og_session_id=af0a84f8847311e3b233bc764e1107f2.173286.1588875313; og_session_id_conf=af0a84f8847311e3b233bc764e1107f2.173286.1588875313; s_visit=1; _fbp=fb.1.1588875313733.844915520; s_cc=true; __gads=ID=d10600aed34d6fd1:T=1588875312:S=ALNI_MaGYlHwled0ITkov_MQymv3gq6wyw; og_autoship=0; _pin_unauth=MWM2MWQyMDEtODFmZi00Zjg4LWFjOTYtNDIxNzRhM2VlNmM0; walmart.nearestLatLng="48.4120872,-89.2413988"; dtSa=-; dtLatC=13; rxVisitor=15887896828899FUFOLKLATMA611L568OGF85KAPCHTRC; enableHTTPS=1; dtSa=-; dtCookie=22$T4CF2FTNEMMV3A34NTKGFK21570UOEBN|5b6d58542e634882|0; AMCV_C4C6370453309C960A490D44%40AdobeOrg=-408604571%7CMCIDTS%7C18394%7CMCMID%7C05034263762608013960105857420568304998%7CMCAAMLH-1589840438%7C7%7CMCAAMB-1589840438%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589242838s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; _gid=GA1.2.899032113.1589235639; s_sq=%5B%5BB%5D%5D; previousBreakpoint=mobile; wmt.breakpoint=m; s_gnr=1589236175304-Repeat; ENV=ak-dfw-prod; bstc=eDbL1gncLdFrMOikJGxiWg; xpa=34JTv|HeXkG|LVSOt|MPTAC|MZ9tt|NOECn|NOaJP|btyTC|eP05T|gbvoH|jeBOs|lZnE7|mOlOu|oygXn|pXPz1|qvGc6|sGGbM|ssJZF|t5K4Y|xzlm3|yI7_k|yntCW|zilS-; exp-ck=34JTv2HeXkG1LVSOt1MPTACkMZ9tt1NOECn2NOaJPHbtyTC1eP05T1gbvoH1jeBOs8lZnE76mOlOuIoygXn1pXPz13qvGc62sGGbM4ssJZF7t5K4Y1xzlm33yI7_k1yntCW1zilS-3; TS01f4281b=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; TS011fb5f6=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; TS0175e29f=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; akaau_P1=1589249999~id=581b7e77ece54e0930f40fae41509094; rxvt=1589250000058|1589248012866; dtPC=22$448200046_67h1vXBTXAKEWMXNSBIGMPYXXOSAJDFBSPUIS-0; _4c_= jVNdb5swFP0rlaX1KYA%2FwJhIVZVmVbdpadeuUx%2BRazvBKgFknLIsyn%2FfNU368VZe4J57zuVe3%2BMdGirToCnJREFTQTEljE%2FQk9n2aLpDzurwekZTZHJecEVkJJZGRWnBRVSoXEcqX7LMCJ4taY4m6G%2BoVfC0EIzjNC32E6SbYw1tlnJT%2BzdahjNOc8IF0OyRJT%2FmGc8Zg7wbDoRjIuNFWnygjghQVXeg7tDG1VCy8r7rp0kyDEM8yHotnY%2BVTEyTrFyrjNsm1xEhoX%2FVagMCUsQiziD2%2FyCKGMbw3blWb5Qv%2FbYLnME8nvT6CRLaPFtlysFqXwUxFfgNrYxdVR7gnI5o5wJlLD7YRrfDqw5O%2Fw18lXESZI%2BuHXoTpPPKtWtzIgigLWwJPYyCHkJnlsa5kfXJic%2BtsvqsgoJfKO7kypTffpVz6c2qddvy3tamvHrhlw8L%2BENv%2FTj6a8UDBoYBOJxR2GCYrW6VrAMX7DVBV7Pyz%2Fev4zQ54yxN0xgsJ%2BBIWB7YN4v7u%2FLicja%2FuX7XfLturN84E%2FV9%2FX6Kx6Tvk2FtlWyklmEtCUl%2B%2FI5oTESMo5%2BzO5b0jImMCzA15oTm57PbizNyuoZpcYZZSjnLOeVYYMIKjgnORJanFEwkGE6LQpzObi%2FPyLG1xXzs%2FnNSEN07u1oZtzC%2BauEKQSy19bZtZI1ebsS7y6DDmlUt%2B94qbfon33ZofzC2KBijnLCcEjCjBzMLnuLw7Pf7%2Fw%3D%3D; _uetsid=_uetec6faf63-2714-a1a6-39d3-e374a14f0eef; xpm=1%2B1589247775%2BWlrDORHfE5eaKvhzqakNKE~%2B0; _derived_epik=dj0yJnU9SGV3OEVrcW8yWWNnSDliUWplMDc0MzJuNEdtcEVzelUmbj0tT1RPTTV6ZC1kUjZLOGZOTlBkYUNBJm09NyZ0PUFBQUFBRjY2QU1v; seqnum=5,Host: www.walmart.ca',
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        #     "X-Requested-With": "XMLHttpRequest"
        # }
        
        url_item = response.xpath('//div[@class="thumb-inner-wrap"]/a/@href').extract_first()
        url_item = str(url_item)
        print('url_item', url_item)
        base_url = 'https://www.walmart.ca'
        data_item = base_url+url_item
        # url_item = response.xpath('//*[@id="thumb-875806"]/div/a')
        if data_item:
            yield scrapy.Request(url=data_item, callback=self.parse_extract)
        # raw_data = response.body
        # data = json.loads(raw_data)
        # print('raw_data',raw_data)     

    def parse_extract(self, response):

        name = response.xpath('//h1[@class="css-1c6krh5 e1yn5b3f7"]/text()').extract()
        
        # walmart_item['name'] = name
        print('name', name)
        # walmart_item = WalmartItem() 
        # name = response.xpath("normalize-space(/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/section[3]/div[2]/div/div[1]/div[7]/div[2]/text())").extract()
        # print('name', name)
        # sku = response.xpath('normalize-space(/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/section[3]/div[2]/div/div[1]/div[6]/div[2]/text())').extract()
        # print('sku', sku)
        # brand = response.xpath('normalize-space(/html/body/div[1]/div/div[3]/div/div/div[2]/div/div/section[3]/div[2]/div/div[1]/div[3]/div[2]/text())').extract()
        # print('brand', brand)
        # name = response.xpath("//h1[@class= 'css-1c6krh5 e1yn5b3f7']/text()").extract()
        # print('name', name)
        # description = response.xpath('normalize-space(//div[@class= "css-gur09u e1mpbtcv1"]/text())').extract()
        # print('description', description)
        # package = response.xpath('normalize-space(//div[@class= "css-1hxe5mn e6y1pbs0"]/text())').extract()
        # print('package', package)
        # imageUrl = response.xpath('normalize-space(//*[starts-with(@property, "og:image")]/@content/text())').extract()
        # print('imageUrl', imageUrl)
        # category = response.xpath('normalize-space(//li[@class= "css-1wco68u e16uoh2c4"]/text())').extract()
        # print('category', category)
        # productUrl = response.xpath('normalize-space(//*[starts-with(@property, "og:url")]/@content/text())').extract()
        # print('productUrl', productUrl)
        # dataJson = response.xpath('normalize-space(/html/body/script[1]/text())').extract()
        # print('dataJson', dataJson)

        #branchProducts information
        # walmart_item['product'] = response.xpath('')#productID 
        # walmart_item['branch'] = response.xpath('') #store ID
        # walmart_item['stock'] = response.xpath('normalize-space(//span[@class="css-1l7huhm e17mwry0"]/text())').extract()
        # walmart_item['price'] = response.xpath('normalize-space(//span[@class="css-2vqe5n esdkp3p0"]/text())').extract()
        # self.item_count += 1
        # if self.item_count > 5:
        #     raise CloseSpider('item_exceeded')
        # yield walmart_item    



   
        
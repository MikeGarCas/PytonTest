# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from walmart.items import WalmartItem

class WalSpider(CrawlSpider):
    #nombre del scraping
    name = 'walmart'
    #contador para parar en 500 elementos
    item_count = 0

    #función para inicializar la busqueda
    def start_requests(self):
        #Url en la que se inicia el scraping
        url = "https://www.walmart.ca/en/grocery/N-117"
        #se insertan los headers para trabajar directo sin javascript en el navegador
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Content-Type": "application/json; charset=UTF-8",
            "Cookie": 'walmart.shippingPostalCode=P7B3Z7; defaultNearestStoreId=3124; zone=9; deliveryCatchment=3124; walmart.csrf=f88f4b5149adef8d907736a1; wmt.c=0; vtc=WlrDORHfE5eaKvhzqakNKE; userSegment=10-percent; TBV=7; rxVisitor=15887896828899FUFOLKLATMA611L568OGF85KAPCHTRC; headerType=grocery; AMCVS_C4C6370453309C960A490D44%40AdobeOrg=1; walmart.id=08ab1e32-3a4a-49fd-88ae-28218bf762bf; usrState=1; _ga=GA1.2.484015444.1588875313; s_ecid=MCMID%7C05034263762608013960105857420568304998; walmart.nearestPostalCode=P7B3Z7; walmart.locale=en; _gcl_au=1.1.779450552.1588875313; og_session_id=af0a84f8847311e3b233bc764e1107f2.173286.1588875313; og_session_id_conf=af0a84f8847311e3b233bc764e1107f2.173286.1588875313; s_visit=1; _fbp=fb.1.1588875313733.844915520; s_cc=true; __gads=ID=d10600aed34d6fd1:T=1588875312:S=ALNI_MaGYlHwled0ITkov_MQymv3gq6wyw; og_autoship=0; _pin_unauth=MWM2MWQyMDEtODFmZi00Zjg4LWFjOTYtNDIxNzRhM2VlNmM0; walmart.nearestLatLng="48.4120872,-89.2413988"; dtSa=-; dtLatC=13; rxVisitor=15887896828899FUFOLKLATMA611L568OGF85KAPCHTRC; enableHTTPS=1; dtSa=-; dtCookie=22$T4CF2FTNEMMV3A34NTKGFK21570UOEBN|5b6d58542e634882|0; AMCV_C4C6370453309C960A490D44%40AdobeOrg=-408604571%7CMCIDTS%7C18394%7CMCMID%7C05034263762608013960105857420568304998%7CMCAAMLH-1589840438%7C7%7CMCAAMB-1589840438%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589242838s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; _gid=GA1.2.899032113.1589235639; s_sq=%5B%5BB%5D%5D; previousBreakpoint=mobile; wmt.breakpoint=m; s_gnr=1589236175304-Repeat; ENV=ak-dfw-prod; bstc=eDbL1gncLdFrMOikJGxiWg; xpa=34JTv|HeXkG|LVSOt|MPTAC|MZ9tt|NOECn|NOaJP|btyTC|eP05T|gbvoH|jeBOs|lZnE7|mOlOu|oygXn|pXPz1|qvGc6|sGGbM|ssJZF|t5K4Y|xzlm3|yI7_k|yntCW|zilS-; exp-ck=34JTv2HeXkG1LVSOt1MPTACkMZ9tt1NOECn2NOaJPHbtyTC1eP05T1gbvoH1jeBOs8lZnE76mOlOuIoygXn1pXPz13qvGc62sGGbM4ssJZF7t5K4Y1xzlm33yI7_k1yntCW1zilS-3; TS01f4281b=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; TS011fb5f6=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; TS0175e29f=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; akaau_P1=1589249999~id=581b7e77ece54e0930f40fae41509094; rxvt=1589250000058|1589248012866; dtPC=22$448200046_67h1vXBTXAKEWMXNSBIGMPYXXOSAJDFBSPUIS-0; _4c_= jVNdb5swFP0rlaX1KYA%2FwJhIVZVmVbdpadeuUx%2BRazvBKgFknLIsyn%2FfNU368VZe4J57zuVe3%2BMdGirToCnJREFTQTEljE%2FQk9n2aLpDzurwekZTZHJecEVkJJZGRWnBRVSoXEcqX7LMCJ4taY4m6G%2BoVfC0EIzjNC32E6SbYw1tlnJT%2BzdahjNOc8IF0OyRJT%2FmGc8Zg7wbDoRjIuNFWnygjghQVXeg7tDG1VCy8r7rp0kyDEM8yHotnY%2BVTEyTrFyrjNsm1xEhoX%2FVagMCUsQiziD2%2FyCKGMbw3blWb5Qv%2FbYLnME8nvT6CRLaPFtlysFqXwUxFfgNrYxdVR7gnI5o5wJlLD7YRrfDqw5O%2Fw18lXESZI%2BuHXoTpPPKtWtzIgigLWwJPYyCHkJnlsa5kfXJic%2BtsvqsgoJfKO7kypTffpVz6c2qddvy3tamvHrhlw8L%2BENv%2FTj6a8UDBoYBOJxR2GCYrW6VrAMX7DVBV7Pyz%2Fev4zQ54yxN0xgsJ%2BBIWB7YN4v7u%2FLicja%2FuX7XfLturN84E%2FV9%2FX6Kx6Tvk2FtlWyklmEtCUl%2B%2FI5oTESMo5%2BzO5b0jImMCzA15oTm57PbizNyuoZpcYZZSjnLOeVYYMIKjgnORJanFEwkGE6LQpzObi%2FPyLG1xXzs%2FnNSEN07u1oZtzC%2BauEKQSy19bZtZI1ebsS7y6DDmlUt%2B94qbfon33ZofzC2KBijnLCcEjCjBzMLnuLw7Pf7%2Fw%3D%3D; _uetsid=_uetec6faf63-2714-a1a6-39d3-e374a14f0eef; xpm=1%2B1589247775%2BWlrDORHfE5eaKvhzqakNKE~%2B0; _derived_epik=dj0yJnU9SGV3OEVrcW8yWWNnSDliUWplMDc0MzJuNEdtcEVzelUmbj0tT1RPTTV6ZC1kUjZLOGZOTlBkYUNBJm09NyZ0PUFBQUFBRjY2QU1v; seqnum=5,Host: www.walmart.ca',            
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        #se ingresa a la url mandando el metodo y los datos de cabecera y manda envia la data a la siguiente función
        yield scrapy.Request(url=url, method="POST", headers=headers, callback=self.parse)

    #Función que entra a las categorías y extrae las url de cada una para ingresar
    def parse(self, response):
        #variable para concatenar la url completa
        base_url = 'https://www.walmart.ca'
        # url = "https://www.walmart.ca/en/grocery/fruits-vegetables/N-3799/"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Content-Type": "application/json; charset=UTF-8",
            "Cookie": 'walmart.shippingPostalCode=P7B3Z7; defaultNearestStoreId=3124; zone=9; deliveryCatchment=3124; walmart.csrf=f88f4b5149adef8d907736a1; wmt.c=0; vtc=WlrDORHfE5eaKvhzqakNKE; userSegment=10-percent; TBV=7; rxVisitor=15887896828899FUFOLKLATMA611L568OGF85KAPCHTRC; headerType=grocery; AMCVS_C4C6370453309C960A490D44%40AdobeOrg=1; walmart.id=08ab1e32-3a4a-49fd-88ae-28218bf762bf; usrState=1; _ga=GA1.2.484015444.1588875313; s_ecid=MCMID%7C05034263762608013960105857420568304998; walmart.nearestPostalCode=P7B3Z7; walmart.locale=en; _gcl_au=1.1.779450552.1588875313; og_session_id=af0a84f8847311e3b233bc764e1107f2.173286.1588875313; og_session_id_conf=af0a84f8847311e3b233bc764e1107f2.173286.1588875313; s_visit=1; _fbp=fb.1.1588875313733.844915520; s_cc=true; __gads=ID=d10600aed34d6fd1:T=1588875312:S=ALNI_MaGYlHwled0ITkov_MQymv3gq6wyw; og_autoship=0; _pin_unauth=MWM2MWQyMDEtODFmZi00Zjg4LWFjOTYtNDIxNzRhM2VlNmM0; walmart.nearestLatLng="48.4120872,-89.2413988"; dtSa=-; dtLatC=13; rxVisitor=15887896828899FUFOLKLATMA611L568OGF85KAPCHTRC; enableHTTPS=1; dtSa=-; dtCookie=22$T4CF2FTNEMMV3A34NTKGFK21570UOEBN|5b6d58542e634882|0; AMCV_C4C6370453309C960A490D44%40AdobeOrg=-408604571%7CMCIDTS%7C18394%7CMCMID%7C05034263762608013960105857420568304998%7CMCAAMLH-1589840438%7C7%7CMCAAMB-1589840438%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589242838s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; _gid=GA1.2.899032113.1589235639; s_sq=%5B%5BB%5D%5D; previousBreakpoint=mobile; wmt.breakpoint=m; s_gnr=1589236175304-Repeat; ENV=ak-dfw-prod; bstc=eDbL1gncLdFrMOikJGxiWg; xpa=34JTv|HeXkG|LVSOt|MPTAC|MZ9tt|NOECn|NOaJP|btyTC|eP05T|gbvoH|jeBOs|lZnE7|mOlOu|oygXn|pXPz1|qvGc6|sGGbM|ssJZF|t5K4Y|xzlm3|yI7_k|yntCW|zilS-; exp-ck=34JTv2HeXkG1LVSOt1MPTACkMZ9tt1NOECn2NOaJPHbtyTC1eP05T1gbvoH1jeBOs8lZnE76mOlOuIoygXn1pXPz13qvGc62sGGbM4ssJZF7t5K4Y1xzlm33yI7_k1yntCW1zilS-3; TS01f4281b=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; TS011fb5f6=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; TS0175e29f=0130aff232eb4a78ddaf0b5a7c1d09f58578481daa095ab07b2ec941a068665d5a728d11d41fd248c0724e8e5044e041c872d23a06; akaau_P1=1589249999~id=581b7e77ece54e0930f40fae41509094; rxvt=1589250000058|1589248012866; dtPC=22$448200046_67h1vXBTXAKEWMXNSBIGMPYXXOSAJDFBSPUIS-0; _4c_= jVNdb5swFP0rlaX1KYA%2FwJhIVZVmVbdpadeuUx%2BRazvBKgFknLIsyn%2FfNU368VZe4J57zuVe3%2BMdGirToCnJREFTQTEljE%2FQk9n2aLpDzurwekZTZHJecEVkJJZGRWnBRVSoXEcqX7LMCJ4taY4m6G%2BoVfC0EIzjNC32E6SbYw1tlnJT%2BzdahjNOc8IF0OyRJT%2FmGc8Zg7wbDoRjIuNFWnygjghQVXeg7tDG1VCy8r7rp0kyDEM8yHotnY%2BVTEyTrFyrjNsm1xEhoX%2FVagMCUsQiziD2%2FyCKGMbw3blWb5Qv%2FbYLnME8nvT6CRLaPFtlysFqXwUxFfgNrYxdVR7gnI5o5wJlLD7YRrfDqw5O%2Fw18lXESZI%2BuHXoTpPPKtWtzIgigLWwJPYyCHkJnlsa5kfXJic%2BtsvqsgoJfKO7kypTffpVz6c2qddvy3tamvHrhlw8L%2BENv%2FTj6a8UDBoYBOJxR2GCYrW6VrAMX7DVBV7Pyz%2Fev4zQ54yxN0xgsJ%2BBIWB7YN4v7u%2FLicja%2FuX7XfLturN84E%2FV9%2FX6Kx6Tvk2FtlWyklmEtCUl%2B%2FI5oTESMo5%2BzO5b0jImMCzA15oTm57PbizNyuoZpcYZZSjnLOeVYYMIKjgnORJanFEwkGE6LQpzObi%2FPyLG1xXzs%2FnNSEN07u1oZtzC%2BauEKQSy19bZtZI1ebsS7y6DDmlUt%2B94qbfon33ZofzC2KBijnLCcEjCjBzMLnuLw7Pf7%2Fw%3D%3D; _uetsid=_uetec6faf63-2714-a1a6-39d3-e374a14f0eef; xpm=1%2B1589247775%2BWlrDORHfE5eaKvhzqakNKE~%2B0; _derived_epik=dj0yJnU9SGV3OEVrcW8yWWNnSDliUWplMDc0MzJuNEdtcEVzelUmbj0tT1RPTTV6ZC1kUjZLOGZOTlBkYUNBJm09NyZ0PUFBQUFBRjY2QU1v; seqnum=5,Host: www.walmart.ca',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        #variable donde se guardan todas las url
        url = response.xpath('//div[@class="media-tracking tile desktop6 tablet3 mobile2  seoTile"]/a/@href').extract()
        # print('url', url)
        #condición para saber si la variable tiene datos
        if len(url) > 0:
            #se envían los datos y se manda llamar la siguiente función
            for allUrl in url:
                url_category = base_url+allUrl
                # print('url_category', url_category)
                yield scrapy.Request(url=url_category, method="POST",  headers=headers, callback=self.parse_item)
        else:
            print('Url not found')    
     
    # función para obtener todas las url de los productos
    def parse_item(self, response):
        
        # se toman las url de cada producto
        urls_item = response.xpath('//a[@class="product-link"]/@href').extract()
        
        #método para eliminar las url repetidas
        myList = list(set(urls_item))
        #variable para completar la url
        base_url = 'https://www.walmart.ca'

        #validación que si existe la url
        if urls_item != 'None':
            for url in myList:
                url_section = base_url+url
                yield scrapy.Request(url=url_section, callback=self.parse_extract)
        else:
            print('URL not found')
    
    #función para obtener toda la data correspondiente
    def parse_extract(self, response):

        base_url = 'https://www.walmart.ca/en'

        # variable para invocar la función desde items
        wl_item = WalmartItem()
        dataComplete = []
        #Aquí es donde se van a extraer todos los datos del item, como es sku, codigo, nombre, etc.
        data = response.xpath('/html/body/script[1]/text()').extract_first()
        #validación para saber si existe data
        if len(data) > 0:
           
            #se reemplazan atributos para manejar el json
            data = data.replace(';', '}')
            data = data.replace('window.__PRELOADED_STATE__', '{"allData"')
            data = data.replace('=',':')
            newData = json.loads(data)

            #ID tienda
            branch = newData["allData"]["catchment"]["storeId"]
            print('branch', branch)
            if branch == 3106 or 3124:
               
                # stock = response.xpath('//span[@class="css-1nqkqc7 esdkp3p2"]').extract() ##no working yet
                #category = response.xpath('') ##not working yet
                productId  = newData["allData"]["product"]["activeSkuId"] ## es el sku de la tabla
                print('productId', productId)
                store = 'Walmart'
                print('store', store)
                upc = newData["allData"]["entities"]["skus"][productId]["upc"] #brancode
                print('upc', upc)
                sku = newData["allData"]["product"]["item"]["id"]
                print('sku', sku)
                # category = response.xpath('//ol[@class="css-f0oitm e16uoh2c1"]').extract_first()
                # print('category', category)
                name = newData["allData"]["product"]["item"]["name"]["en"]
                print('name', name)
                description = newData["allData"]["entities"]["skus"][productId]["longDescription"]
                print('description', description)
                package = newData["allData"]["product"]["item"]["description"]
                print('package', package)
                imageUrl = newData["allData"]["entities"]["skus"][productId]["images"][0]["large"]["url"]
                imageUrl = base_url+imageUrl
                print('imageUrl', imageUrl)
                url1 = response.xpath('//link[@rel="alternate"]/@href')[0].extract()
                print('url1', url1)
                brand = newData["allData"]["entities"]["skus"][productId]["brand"]["name"]
                print('brand', brand)

                idProduct = 'idProduc'
                tienda = 'tienda'
                newUpc = 'upc'
                eseku = 'eseku'
                nombre = 'nombre'
                descripcion = 'descripcion'
                paquete = 'paquete'
                imagenUrl = 'imagenUrl'
                url2 = 'url2'
                brande = 'brande'

                dataComplete.append({
                    idProduct : productId,
                    tienda : store,
                    newUpc : upc,
                    eseku : sku,
                    nombre : name,
                    descripcion : description,
                    paquete : package,
                    imagenUrl : imageUrl,
                    url2 : url1,
                    brande : brand
                })
                print(dataComplete)

                wl_item['productId'] = productId
                wl_item['store'] = store
                wl_item['upc'] = upc
                wl_item['sku'] = sku
                # wl_item['category'] = category
                wl_item['name'] = name
                wl_item['description'] = description
                wl_item['package'] = package
                wl_item['imageUrl'] = imageUrl
                wl_item['url1'] = url1
                wl_item['brand'] = brand
                # if len(dataComplete) > 10:
                #     raise CloseSpider('item_exceeded')
                #     print(dataComplete)
                self.item_count += 1
                if self.item_count > 5:
                    raise CloseSpider('item_exceeded')
                yield wl_item                   
            else:
                print('La rama no pertenece a la 3106 o la 3124')    
            
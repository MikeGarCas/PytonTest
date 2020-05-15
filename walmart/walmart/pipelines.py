# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from spiders.models import Base, Product, BranchProduct

class WalmartPipeline:  

    def __init__(self):
        engine = create_engine("sqlite:///db.sqlite")
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
    	
    	session = self.Session()
    	product = Product()
    	branch_product = BranchProduct()

        product.store = item["store"]
        product.sku = item["sku"]
        product.barcodes = item["upc"]
        product.brand = item["brand"]
        product.name = item["name"]
        product.description = item["description"]
        product.package = item["package"]
        product.image_urls = item["imageUrl"]

        branch_product.branch = item['branch']
        branch_product.stock = item['stock']
        
        product.branch_products.append(branch_product)
        session.add(product)
        session.commit()
        return item

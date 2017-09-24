# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
from datetime import datetime
import pandas as pd
import pickle
import os
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level = logging.INFO,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger()

class XePipeline(object):
    def open_spider(self, spider):
        self.df = pd.DataFrame()


    def close_spider(self, spider):
        directory = u"E:/Documents/OneDrive/4_Προγραμματισμός/Scrapy/Αγορά Ακινήτων/"+spider.name+u"/Αρχεία_pd.DataFrame"
        os.chdir(directory)
        now = datetime.now()
        filename = spider.name+" "+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+" "+'Items.pickle'
        with open(filename, 'w') as file:
            pickle.dump(self.df,file)
        # Check for empty fields
        colList = self.df.columns.tolist()
        for col in colList:
            if self.df[col].isnull().all():
                logger.warning("Found Null Field, in file " + filename +": " + col)
        # This line is a test

    def process_item(self, item, spider):
        self.df = self.df.append(item,ignore_index=True)

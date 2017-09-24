# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import smtplib

class XePipeline(object):

    def close_spider(self, spider):
<<<<<<< HEAD
        mail = smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        emailAddress = 'ivmpythonscripts@gmail.com'
        pwd = 'Gh74d8G5GDJU6ds3'
        mail.login(emailAddress,pwd)
        reciever = 'vouvakismanousakis@outlook.com'
        mail_content = "Spider "+spider.name+" closed"
        mail.sendmail(emailAddress,reciever,mail_content)
        mail.close()
=======
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
>>>>>>> parent of a37fc18... Test line removed

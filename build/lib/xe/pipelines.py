# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import smtplib

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level = logging.INFO,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger()

class XePipeline(object):
    def open_spider(self, spider):
        pass


    def close_spider(self, spider):
        content = "Spider "+spider.name+" closed"
        send_mail(self,spider,content)

    def process_item(self, item, spider):
        pass

    def send_mail(self,spider,mail_content):
        logger.INFO("Sending Email")
        mail = smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        emailAddress = 'ivmpythonscripts@gmail.com'
        pwd = 'Gh74d8G5GDJU6ds3'
        mail.login(emailAddress,pwd)
        reciever = 'vouvakismanousakis@outlook.com'
        mail.sendmail(emailAddress,reciever,mail_content)
        mail.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import smtplib

class XePipeline(object):

    def close_spider(self, spider):
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

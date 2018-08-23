# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class HouseDataPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    '''
    插入mysql数据库
    '''
    def __init__(self):
        self.conn =pymysql.connect(host='localhost',port=3306,user='root',passwd='liwenwu.610',db='cqhouse',use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql = '''
        insert into house_data(url,price_per,price_total,room_number,living_room_number,high,house_toward,house_type,size,build_year,buding_type,dianti,name,location,rail) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''

        self.cursor.execute(insert_sql,(item["url"],item["price_per"],item["price_total"],item["room_number"],item["living_room_number"],item["high"],item["house_toward"],item["house_type"],item["size"],item["build_year"],item["buding_type"],item["dianti"],item["name"],item["location"],item["rail"]))
        self.conn.commit()
#    insert into house_data(url,price_per,price_total,style,louceng,high,house_toward,house_type,size,build_year,buding_type,name,location) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
# create table house_data(url char(100),price_per char(20),price_total char(100),room_number char(10),living_room_number char(20),high char(20),house_toward char(20),house_type char(20),size char(20),build_year char(20),buding_type char(20),dianti char(5),name char(50),location char(20),rail char(10));
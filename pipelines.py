# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector


class GlassdoorPipeline(object):

    def __init__(self):
        self.create_connection()  # whenevr the class is initialized the two methods are automatically called
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(host="localhost",
                                            user="root",
                                            passwd="keepcalm",
                                            database="glassdoor")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS jobtable_tb""")
        self.curr.execute("""create table jobtable_tb(
                        title text,
                        empname text,
                        location text,
                        size text,
                        salarylow text,
                        salaryhigh text,
                        jobId text,
                        year text,
                        rating text
                    
                        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into jobtable_tb values(%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item['title'],
            item['empname'],
            item['location'],
            item['size'],
            item['salarylow'],
            item['salaryhigh'],
            item['jobId'],
            item['year'],
            item['rating']

        ))
        self.conn.commit()

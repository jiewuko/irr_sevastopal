# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from os import path

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class IrrSevastopalPipeline(object):
    def process_item(self, item, spider):
        return item


class SQLiteStorePipeline(object):
    filename = 'irr.sqlite'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def check_item_in_db(self):
        rows = []
        try:
            curs = self.conn.execute('SELECT url FROM irr_data')
            rows = list(map(lambda url: url[0], curs.fetchall()))
        except Exception as e:
            print('check was crashed with exception {}'.format(e))
        return rows

    def process_item(self, item, spider):
        if item['url'] in self.urls_from_db:
            print('Это объявление уже есть в базе {}'.format(item['url']))
            return
        try:
            self.conn.execute('insert into irr_data(url,title,description,category,subcategory,type_,owner_name,'
                              'address,published_date,price,telephone,agency) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                              (item['url'], item['title'], item['description'], item['category'],
                               item['subcategory'], item['type_'], item['owner_name'],
                               item['address'], item['published_date'], item['price'],
                               item['telephone'], item['agency'],
                               ))
        except Exception as e:
            print(e)
            print('Failed to insert item: ' + item['url'])
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)
        self.urls_from_db = self.check_item_in_db()

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""CREATE TABLE irr_data
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, title TEXT, description TEXT,
                      category TEXT, subcategory TEXT, type_ TEXT, owner_name TEXT,
                      address TEXT, published_date NUMERIC, price TEXT, telephone TEXT, agency TEXT)""")
        conn.commit()
        return conn

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
from sqlite3 import Error

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SarjisPipeline:

    sql_create_sarjis_table = """CREATE TABLE IF NOT EXISTS sarjis (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    date text,
                                    number text,
                                    title text,
                                    alt text,
                                    img_url text NOT NULL
                                );"""

    sql_insert = ''' INSERT INTO sarjis(name, date, number, title, alt, img_url)
            VALUES(?,?,?,?,?,?) '''

    def __init__(self, db_uri):
        self.db_uri = db_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_uri = crawler.settings.get('DB_URI'),
        )

    def open_spider(self, spider):
        try:
            self.conn = sqlite3.connect(self.db_uri)
            c = self.conn.cursor()
            c.execute(self.sql_create_sarjis_table)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        c = self.conn.cursor()
        c.execute(self.sql_insert, (adapter['name'], adapter['date'], adapter['number'], adapter['title'],adapter['alt'], adapter['imgurl']))
        self.conn.commit()

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            imagepath = value["path"]
        item["front_image_path"] = imagepath
        return item


# 自定义的写入到json文件
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
        print("JSON")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# scapy自带的保存json格式文件的函数
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


# 存储到数据库中函数
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="scrapydb", charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into articles(title,url,created_date,fav_nums)
            VALUES (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["created_date"], item["fav_nums"]))
        self.conn.commit()


# mysql插入异步化
class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls, setting):
        dbparms = dict(host=setting["MYSQL_HOST"],
                       db=setting["MYSQL_DBNAME"],
                       user=setting["MYSQL_USR"],
                       passwd=setting["MYSQL_PASSWORD"],
                       charset="utf-8",
                       cursorclass=MySQLdb.cursors.DictCursor,
                       use_unicode=True)

        # 可变参数
        dbpool=adbapi.ConnectionPool("MYSQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrorback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        print (failure)

    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                   insert into articles(title,url,created_date,fav_nums)
                   VALUES (%s,%s,%s,%s)
               """
        cursor.execute(insert_sql, (item["title"], item["url"], item["created_date"], item["fav_nums"]))
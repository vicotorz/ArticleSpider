# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 使用了scrapy框架下的ImagesPipeline
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            imagepath = value["path"]
        item["front_image_path"] = imagepath
        return item


#1 自定义的写入到json文件
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


#2 scapy自带的保存json格式文件的函数
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
        print("开始存入数据库")
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="scrapydb", charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        print("存入")
        insert_sql = """
            insert into articles(title,create_date,url,url_object_id,front_image_url,comment_nums,fav_nums,praise_nums,tags,content)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (
            item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"],
            item["comment_nums"], item["fav_nums"], item["praise_nums"], item["tags"],
            item["content"]))
        print (dict(item))
        self.conn.commit()


# mysql插入异步化
class MysqlTwistedPipline(object):
    print("异步存入")
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        #query.addErrorback(self.handle_error, item, spider)

    #def handle_error(self, failure, item, spider):
        #print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                    insert into articles(title,create_date,url,url_object_id,front_image_url,comment_nums,fav_nums,praise_nums,tags,content)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (
            item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"],
            item["comment_nums"], item["fav_nums"], item["praise_nums"], item["tags"],
            item["content"]))

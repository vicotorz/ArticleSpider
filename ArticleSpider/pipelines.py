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


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            imagepath = value["path"]
        item["front_image_path"]=imagepath
        return item

#自定义的写入到json文件
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file=codecs.open('article.json','w',encoding="utf-8")
        print ("JSON")
    def process_item(self, item, spider):
        lines=json.dumps(dict(item),ensure_ascii=False)
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()

#scapy自带的保存json格式文件的函数
class JsonExporterPipeline(object):
    def __init__(self):
        self.file=open('articleexporter.json','wb')
        self.exporter =JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

#存储到数据库中函数
class MysqlPipeline(object):
    def __init__(self):
       self.conn=MySQLdb.connect(host="localhost", user="root", passwd="", db="scrapydb", charset="utf8")
       self.cursor=self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql="""
            insert into articles(title,url,created_date,fav_nums)
            VALUES (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["title"],item["url"],item["created_date"],item["fav_nums"]))
        self.conn.commit()


# ArticleSpider
Python Scrapy 爬虫实战

【Python虚拟环境使用总结】（未完成，待继续）
【虚拟环境】
(1)pip install virtualenv

(2)virtualenv -p python路径\python.exe aaa(名字) 或者  mkvirtualenv --python=python路径\python.exe aaa(名字)

(3)pip install virtualenvwrapper-win

(4)在本机设置WORKON_HOME路径(D:\Envs)，并将创建的环境放进新的Envs目录中

(5)workon aaa

(6)在当前虚拟环境中安装scrapy，如果安装不上Twisted，手动安装

(7)创建scrapy工程   scrapy startproject xxx

(8)进入这个工程，然后创建scrapy模版   【命令】scrapy genspider jobbole bolog.jobbole.com

【2017-11-20 笔记】
【xpath+css基础语法】

建议打开虚拟环境，在命令窗口中，输入【命令】scrapy shell + (要爬取的网站)，然后进行xpath/css命令调试`

xpath+css语句

Request模块+urllilb的parse

【深度遍历】

爬虫思路：1，解析页面 2，解析下一页url

定义item，将数据定义解耦到items.py中 setting中的itemPipeLine打开，将item传入到pipeline中(pipeline对item进行拦截)

【图片下载】

图片下载：(Pillow库安装)
    ITEM_PIPELINE加入到pipeline中
    scrapy.pipelines.images.ImagePipeline=1 (数字越小越早进入到pipeline之中)
    IMAGES_URLS_FIELD=""
    IMAGES_STORE="

#图片保存到本地
#配置image url字段
IMAGES_URLS_FIELD = "front_image_url"
project_dir=os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE = os.path.join(project_dir,'images')"
    
【2018-1-4 笔记】
【json--pipeline（自定义/scrapy自带），mysql--pipeline（mysql同步/mysql+twisted 异步）】

增加保存json的pipeline，修复了部分笔误bug

数据增加到mysql

【2018-1-5 笔记】
【异步化mysql】

增加异步twisted插入到数据库

【自定义itemloader】（不太好用）

自定义itemloader

from scrapy.loader import ItemLoader

from scrapy.loader.processors import MapCompose,TakeFirst,Join

在scrapy.Field()中添加input_processor=MapCompose（函数），将在pipeline中进行的数据处理修改到items中

#通过item loader加载item

在主爬虫中添加
（1）item_loader.add_value
（2）item_loader.add_css

创建itemloader，load各个字段

【2018-1-7 笔记】
弃用了itemloader

修复异步mysql问题（setttings 写成 setting）
    


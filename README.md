# ArticleSpider
Python Scrapy 爬虫实战

【Python虚拟环境使用总结】

(1)pip install virtualenv

(2)virtualenv -p python路径\python.exe aaa(名字) 或者  mkvirtualenv --python=python路径\python.exe aaa(名字)

(3)pip install virtualenvwrapper-win

(4)在本机设置WORKON_HOME路径，并将创建的环境放进新的Envs目录中

(5)workon aaa

(6)在当前虚拟环境中安装scrapy，如果安装不上Twisted，手动安装

(7)创建scrapy工程   scrapy startproject xxx

(8)进入这个工程，然后创建scrapy模版   scrapy genspider jobbole bolog.jobbole.com

【2017-11-20 笔记】
xpath+css语句
Request模块+urllilb的parse
爬虫思路：1，解析页面 2，解析下一页url
定义item，将数据定义解耦到items.py中 setting中的itemPipeLine打开，将item传入到pipeline中(pipeline对item进行拦截)
图片下载：(Pillow库安装)
    ITEM_PIPELINE加入到pipeline中
    scrapy.pipelines.images.ImagePipeline=1 数字越小越早进入到pipeline之中
    IMAGES_URLS_FIELD=""
    IMAGES_STORE=""
    
【2018-1-4 笔记】
增加保存json的pipeline，修复了部分笔误bug

    


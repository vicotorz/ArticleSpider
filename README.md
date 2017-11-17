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

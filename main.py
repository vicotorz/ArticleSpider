#-*- codeing:utf-8 -*-
__author__='victorz'

import sys
import os

from scrapy.cmdline import execute

#可调式作用
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","jobbole"])
#!/usr/bin/python
#coding=utf-8
import sys,os,re
reload(sys)
sys.setdefaultencoding('utf8')
from common.selector import *
from common.parser import *
from common.db import *
from common.download import *
import time

url = 'http://car.autohome.com.cn/'
splider=BrowserBase()
html = splider.read(url)
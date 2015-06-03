__author__ = 'ShengYue'
import re
m = re.search(r'/dianshi/list.php\??(&?(cat=\w+|year=\w+|pageno=\d+|area=\w+|act=all)?){0,6}$','http://www.360kan.com/dianshi/list.php?cat=s&year=0all&cat=all&act=all&area=all')
if m:
    print m.group()
else:
    print False

m = re.match(r'hello', 'hello world!')
print m.group()



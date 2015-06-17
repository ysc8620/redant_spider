__author__ = 'ShengYue'
import re
m = re.search(r'/dianshi/list.php((\?|&)(cat=(all|\d+)|year=(other|all|\d+)|pageno=\d+|area=(\d+|all)|act=[%\w]+|rank=(createtime|rankpoint))){0,6}$','http://www.360kan.com/dianshi/list.php?rank=rankpoint&cat=all&year=other&area=all&act=%E9%BB%84%E6%B8%A4')
if m:
    print m.group()
else:
    print False

m = re.match(r'hello', 'hello world!')
print m.group()



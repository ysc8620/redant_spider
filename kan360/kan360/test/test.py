#coding=utf-8
__author__ = 'ShengYue'
import re,json
from scrapy.selector import Selector

class parser_tags:
    allow_tags = []
    del_tags = []
    isEmpty = False
    xml = ''
    parser = None
    def __init__(self, parser=None):
        self.parser = parser

    def xml(self, xml):
        self.xml = xml
        return self

    def rm(self, tag):
        self.del_tags.append(tag)
        return self

    def kp(self, tag):
        self.allow_tags.append(tag)
        return self

    def empty(self):
        self.isEmpty = True
        return  self

    def __rm(self):
        tags = ''
        for tag in self.del_tags:
            tags = tags+'|'+tag
        tags = tags.strip('|')

        if tags:
            link = re.compile(r"</?("+tags+").*?>", re.I)
            self.xml = re.sub( link, '', self.xml)

    def __kp(self):
        tags = ''
        for tag in self.allow_tags:
            tags = tags + '|' + tag + '|/' + tag
        tags = tags.strip('|')

        if tags:
            link = re.compile(r"<[^("+tags+")].*?>",re.I)
            self.xml = re.sub(link,'',self.xml)

    def __empty(self):
        if self.isEmpty:
            link = re.compile(r"\s+")
            self.xml = re.sub(link,' ', self.xml)

    def run(self):
        self.__rm()
        self.__kp()
        self.__empty()
        return self.xml

def parser_url():
    m = re.search(r'/dianshi/list.php((\?|&)(cat=(all|\d+)|year=(other|all|\d+)|pageno=\d+|area=(\d+|all)|act=[%\w]+|rank=(createtime|rankpoint))){0,6}$','http://www.360kan.com/dianshi/list.php?rank=rankpoint&cat=all&year=other&area=all&act=%E9%BB%84%E6%B8%A4')
    if m:
        print m.group()
    else:
        print False

    m = re.match(r'hello', 'hello world!')
    print m.group()

def test():
    data = u'''<div id="content_sohu" class="content" site="sohu"><div class="content-bd gclearfix"><dl><dt><a playno="1" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150612/n414876260.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="首尔市长连夜通报MERS情况 政府应对措施引争议" >首尔市长连夜通报MERS情况 政府应</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="1" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150612/n414876260.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="首尔市长连夜通报MERS情况 政府应对措施引争议" ><img src="http://photocdn.sohu.com/20150612/vrsb1670214.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-06-11期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="2" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150605/n414464201.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E118 美国配送炭疽病菌 第一毛织与三星水产合并" >E118 美国配送炭疽病菌 第一毛织与</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="2" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150605/n414464201.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E118 美国配送炭疽病菌 第一毛织与三星水产合并" ><img src="http://photocdn.sohu.com/20150605/vrsb1663608.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-06-04期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="3" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150529/n414022466.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E117 韩法务部长获总理提名 马云引韩电商担忧" >E117 韩法务部长获总理提名 马云引</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="3" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150529/n414022466.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E117 韩法务部长获总理提名 马云引韩电商担忧" ><img src="http://photocdn.sohu.com/20150529/vrsb1656677.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-05-28期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="4" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150522/n413516682.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E116 李完九被检方传召 潘基文侄子涉诈骗" >E116 李完九被检方传召 潘基文侄子</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="4" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150522/n413516682.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E116 李完九被检方传召 潘基文侄子涉诈骗" ><img src="http://photocdn.sohu.com/20150522/vrsb1649967.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-05-21期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="5" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150515/n413081511.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E115 公务员退休金改革案泡汤 省长受传唤" >E115 公务员退休金改革案泡汤 省长</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="5" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150515/n413081511.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E115 公务员退休金改革案泡汤 省长受传唤" ><img src="http://photocdn.sohu.com/20150515/vrsb1642155.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-05-14期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="6" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150508/n412636265.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E114 韩B级文化成主流 李龙女感性做客" >E114 韩B级文化成主流 李龙女感性</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="6" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150508/n412636265.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E114 韩B级文化成主流 李龙女感性做客" ><img src="http://photocdn.sohu.com/20150508/vrsb1635737.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-05-07期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd><dd class="guests"><em class="gray">嘉宾：</em>李龙女 </dd></dl><dl><dt><a playno="7" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150501/n412222863.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="成完钟名单影响持续 率智模仿任元喜惟妙惟肖" >成完钟名单影响持续 率智模仿任元</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="7" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150501/n412222863.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="成完钟名单影响持续 率智模仿任元喜惟妙惟肖" ><img src="http://photocdn.sohu.com/20150501/vrsb1630403.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-04-30期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="8" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150424/n411792774.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="讽刺李完九作品层出不穷 郑雅兰狂减25kg" >讽刺李完九作品层出不穷 郑雅兰狂</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="8" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150424/n411792774.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="讽刺李完九作品层出不穷 郑雅兰狂减25kg" ><img src="http://photocdn.sohu.com/20150424/vrsb1623632.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-04-23期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="9" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150417/n411406336.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E111 成完钟名单震撼韩国 被称死亡笔记" >E111 成完钟名单震撼韩国 被称死亡</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="9" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150417/n411406336.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E111 成完钟名单震撼韩国 被称死亡笔记" ><img src="http://photocdn.sohu.com/20150417/vrsb1616899.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-04-16期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="10" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150410/n411044493.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E110 韩腐败案上演密室悬疑 女星表白MC" >E110 韩腐败案上演密室悬疑 女星表</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="10" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150410/n411044493.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E110 韩腐败案上演密室悬疑 女星表白MC" ><img src="http://photocdn.sohu.com/20150410/vrsb1610422.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-04-09期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="11" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150403/n410743722.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E109 政府金融支援政策 地域贬低发言罚款" >E109 政府金融支援政策 地域贬低发</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="11" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150403/n410743722.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E109 政府金融支援政策 地域贬低发言罚款" ><img src="http://photocdn.sohu.com/20150403/vrsb1605253.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-04-02期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="12" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150327/n410386215.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E108 揭韩疗养业腐败 韩综界被曝重男轻女" >E108 揭韩疗养业腐败 韩综界被曝重</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="12" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150327/n410386215.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E108 揭韩疗养业腐败 韩综界被曝重男轻女" ><img src="http://photocdn.sohu.com/20150327/vrsb1598992.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-03-26期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="13" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150320/n410043696.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E107 曝韩影史3大死亡 新增MC推荐环节" >E107 曝韩影史3大死亡 新增MC推荐</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="13" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150320/n410043696.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E107 曝韩影史3大死亡 新增MC推荐环节" ><img src="http://photocdn.sohu.com/20150320/vrsb1592832.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-03-19期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="14" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150313/n409719756.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E106 新人结婚费用高 李泰林爆粗口被删戏" >E106 新人结婚费用高 李泰林爆粗口</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="14" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150313/n409719756.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E106 新人结婚费用高 李泰林爆粗口被删戏" ><img src="http://photocdn.sohu.com/20150313/vrsb1585580.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-03-12期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="15" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150306/n409388264.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E105 韩宪法废除通奸罪 曝韩国最贵地皮" >E105 韩宪法废除通奸罪 曝韩国最贵</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="15" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150306/n409388264.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E105 韩宪法废除通奸罪 曝韩国最贵地皮" ><img src="http://photocdn.sohu.com/20150306/vrsb1578904.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-03-05期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="16" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150227/n409186100.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E104 三星与LG互控 李孝利豪宅被观光" >E104 三星与LG互控 李孝利豪宅被观</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="16" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150227/n409186100.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E104 三星与LG互控 李孝利豪宅被观光" ><img src="http://photocdn.sohu.com/20150227/vrsb1572114.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-02-26期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="17" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150220/n409095781.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E103 艺人特别招生分析 支招《我结》危机" >E103 艺人特别招生分析 支招《我结</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="17" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150220/n409095781.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E103 艺人特别招生分析 支招《我结》危机" ><img src="http://photocdn.sohu.com/20150220/vrsb1568368.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-02-19期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="18" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150213/n408976440.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E102 海关罚超免税者 青瓦台垃圾桶90万" >E102 海关罚超免税者 青瓦台垃圾桶</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="18" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150213/n408976440.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E102 海关罚超免税者 青瓦台垃圾桶90万" ><img src="http://photocdn.sohu.com/20150213/vrsb1561941.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-02-12期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="19" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150206/n408786514.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E101 BJ高收入分析 主持人模女神跳舞" >E101 BJ高收入分析 主持人模女神跳</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="19" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150206/n408786514.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E101 BJ高收入分析 主持人模女神跳舞" ><img src="http://photocdn.sohu.com/20150206/vrsb1554664.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-02-05期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl><dl><dt><a playno="20" sitename="sohu" needrecord="record" movieid="21757" playtype="zongyi" href="http://tv.sohu.com/20150130/n408196874.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E100 主持人自我审判 姜龙锡节目撞车遭批" >E100 主持人自我审判 姜龙锡节目撞</a></dt><dd class="poster"><a playtype="zongyi" class="play_btn" playno="20" sitename="sohu" needrecord="record" movieid="21757" href="http://tv.sohu.com/20150130/n408196874.shtml?txid=19b06d0609b2eda1bcef9b6ce824056a" title="E100 主持人自我审判 姜龙锡节目撞车遭批" ><img src="http://photocdn.sohu.com/20150130/vrsb1547426.jpg" /><div class="intro-bg"></div><div class="intro-txt">2015-01-29期</div><div class="hide-bg"></div><div class="hide-btn hover"></div></a></dd></dl></div><div  class="content-ft gclearfix"><a pageNum="1" class="firstPage"><span>«首页</span></a><a pageNum="1" class="pageUp"><span>«上一页</span></a><span class="number"><a pageNum="1"  class="cur"><span>1</span></a><a pageNum="2" ><span>2</span></a><a pageNum="3" ><span>3</span></a><a pageNum="4" ><span>4</span></a><a pageNum="5" ><span>5</span></a></span><a pageNum="2" class="pageDown"><span>下一页»</span></a><a pageNum="5" class="lastPage"><span>最后一页»</span></a></div></div>'''

    hs = Selector(text=data)
    dl = hs.xpath("//dl").extract()
    for i in dl:
        dls =   Selector(text=i)
        href = dls.xpath('//a/@href').extract()
        text = dls.xpath('//div[@class="intro-txt"]/text()').extract()

        img = dls.xpath('//img/@src').extract()
        title = dls.xpath('//a/@title').extract()

        print href[0],text[0],img[0],title[0]
def sp():
    _Tags = parser_tags()
    print _Tags.xml('x').rm('p').rm('span').rm('em').empty().run()
if __name__ == '__main__':
    sp()



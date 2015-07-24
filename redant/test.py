__author__ = 'ShengYue'

from common.selector import *
from common.download import *



if __name__ == '__main__':
    #splider = BrowserBase()
    #data = splider.read('http://www.360kan.com/m/f6fjYxH1QHH6UR.html')
    data = file('test.html').read()

    root = Selector(data,'http://www.360kan.com/m/f6fjYxH1QHH6UR.html')
    links = root.xpath("//div[@class='aggregate-rating']//div[@class='rating-count']/text()").re("\d+")
    #print links[0]
    #print root.get_link('dfg/xxxxxx.html')


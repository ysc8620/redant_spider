__author__ = 'ShengYue'
import sys,re
reload(sys)
sys.setdefaultencoding('utf8')
from common.download import *
from w3lib.html import replace_entities
from w3lib.encoding import html_to_unicode
from lxml import etree
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath

__all__ = ['Selector', 'SelectorList']
_ctgroup = {
    'html': {'_parser': etree.HTMLParser,
             '_tostring_method': 'html'},
    'xml': {'_parser': etree.HTMLParser,
            '_tostring_method': 'xml'},
    }

def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, (8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        if hasattr(el, "__iter__"):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def extract_regex(regex, text, encoding='utf-8'):
    """Extract a list of unicode strings from the given text/encoding using the following policies:

    * if the regex contains a named group called "extract" that will be returned
    * if the regex contains multiple numbered groups, all those will be returned (flattened)
    * if the regex doesn't contain any group the entire regex matching is returned
    """

    if isinstance(regex, basestring):
        regex = re.compile(regex, re.UNICODE)

    try:

        strings = [regex.search(text).group('extract')]   # named group
    except:
        strings = regex.findall(text)    # full regex or numbered groups
    strings = flatten(strings)

    if isinstance(text, unicode):
        for s in strings:
            return replace_entities(s, keep=['lt', 'amp'])
    else:
        for s in strings:
            replace_entities(unicode(s, encoding), keep=['lt', 'amp'])

class Selector():

    _root = None
    _lxml_smart_strings = False
    def factory(self,data, parser_cls,url):
        charset = 'charset=%s' % 'utf-8'

        data = html_to_unicode(charset, data)[1]

        body = data.encode('utf8') or '<html/>'

        parser = parser_cls(recover=True, encoding='utf8')

        self._root = etree.fromstring(body, parser=parser, base_url=url)

        return self._root

    def __init__(self,data='',url='',parser='html'):
        self.namespaces = {}
        self.type = parser
        self.base_url = url
        self.result = []
        self._parser = _ctgroup[parser]['_parser']
        self._tostring_method = _ctgroup[parser]['_tostring_method']

        self.factory(data, self._parser,url)

    def get_base_link(self,base_url, url):
        url1 = urljoin(base_url, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

    def get_link(self,url,base_url=None):
        if base_url ==None:
            url1 = urljoin(self.base_url, url)
        else:
            url1 = urljoin(base_url, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

    def xpath(self, query):
        try:
            xpathev = self._root.xpath
        except AttributeError:
            return []

        try:
            result = xpathev(query, namespaces=self.namespaces,
                             smart_strings=self._lxml_smart_strings)
        except etree.XPathError:
            msg = u"Invalid XPath: %s" % query
            raise ValueError( msg.encode("unicode_escape"))
        self.result = result
        return self

    def extract(self):
        ret = []
        try:
            for i in self.result:
                ret.append( etree.tostring(i,
                                      method=self._tostring_method,
                                      encoding=unicode,
                                      with_tail=False))
        except (AttributeError, TypeError):
            for i in self.result:
                ret.append(  unicode(i))
        return ret

    def re(self, regex):
        ret = self.extract()
        result = []
        for i in ret:
            result.append(extract_regex(regex, i))
        return result

class SelectorList(list):

    def __getslice__(self, i, j):
        return self.__class__(list.__getslice__(self, i, j))

    def xpath(self, xpath):
        return self.__class__(flatten([x.xpath(xpath) for x in self]))

    def css(self, xpath):
        return self.__class__(flatten([x.css(xpath) for x in self]))

    def re(self, regex):
        return flatten([x.re(regex) for x in self])

    def extract(self):
        return [x.extract() for x in self]


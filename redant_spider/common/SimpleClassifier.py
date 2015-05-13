#!/usr/bin/python
#coding=utf-8
import sys,os
from inflector import *
from redant_spider.common.db import *
reload(sys)
sys.setdefaultencoding('utf8')

'''
/**
 * <h1>识别出商品的类别</h1>
 *
 * 1.从商品 title 中分词得到一批词语
 * 2.去le_goods_cate_keywords查询，
 * 3.查询的时候，先用 = ，如果查不到，就用 like xx% 再没有，就用 like %xx%
 * 4.取权重最高的。
 *
 * @author weiwei
 *
 */
 '''
class CateAndTags:
    def __init__(self):
        pass

class Segments:
    @classmethod
    def filter(self, text):
        return get_simple_text(text)

    @classmethod
    def seg(self,text = ''):
		if text == '' or len(text.strip()) == 0:
			return ''

		#1.过滤常用字符
		pureText = Segments.filter(text)
		#2.按空格隔开
		data = pureText.split('-')
		return data
        # //		List<String> result = new ArrayList<String>();
        # //		// 3.正向最大匹配,需要给定一个最大匹配个数值，默认2个单词
        # //		for (int i = 0; i < array.length; i++){
        # //			String str = array[i];
        # ////			System.out.println("str----->"+str);
        # //			StringBuilder sb = new StringBuilder(str);
        # //			if (findByKeyword(str) != null)
        # //				result.add(str);
        # //
        # //			for (int j = i+1; j < array.length; j++){
        # //				sb.append(" ").append(array[j]);
        # //
        # //				//注意要小于规定的最大匹配个数值
        # //				if (sb.toString().split(" ").length > max)
        # //					break;
        # //
        # //				if (findByKeyword(sb.toString()) == null)
        # //					continue;
        # //
        # //				result.add(sb.toString());
        # //			}
        # //		}
        # //
        # //		return result

class SimpleClassifier:
    cateWeight = {}

    def findCateAndTags(self,text, max=3):
        result = {'cates':[], 'cate':0}
        cates = self.sortCateByWeight(self.countCateWeight(Segments.seg(text), max))
        #print cates
        if (cates == False or len(cates)<1):
			return result
        topCateId = False
        for cate_id in cates:
			if (cate_id == False):
				continue
			topCate = self.findTopCate(cate_id)
			if (topCate == False):
				continue
			topCateId = topCate['id']
			break
        result['cate'] = topCateId
        if topCateId != False  and topCateId > 0:
            try:
			    cates.remove (str(topCateId))
            except:
                pass
        if len(cates)<1:
			return result
        for cate_id in cates:
            topCate = self.findTopCate(cate_id)
            if topCate != False:
                _topId = topCate["id"]
                if _topId != False and result['cate'] != _topId:
					continue
            result['cates'].append(cate_id)
        return result

    def countCateWeight(self, keywords, maxSize=0):
        if (keywords == False or len(keywords)<1):
            return False
        max = maxSize
        if (max <= 0):
            max = 3
        self.cateWeight = {}
        #1.使用 like equal like 'xx' 查询
        i = 0
        for keyword in keywords:
            # 3.正向最大匹配,需要给定一个最大匹配个数值，默认2个单词
            records = self.findByKeyword(keyword)
            if (records != False):
                self.countWeight(records, keyword)

            for j in range(max):
                long_keywords = keywords[i:i+j]
                long_keywords =  ' '.join(long_keywords)
                if long_keywords == keyword:
                    continue
                records = self.findByKeyword(keyword)
                if (records == False):
                    continue
                self.countWeight(records, keyword)
            i = i + 1

        if len(self.cateWeight) <1:
            return False
        data = {}
        for k in self.cateWeight:
            data.setdefault(k,self.cateWeight[k])
        return data

    def countWeight(self,records, keyword):
        _weight = 5
        for cate in records:
            cate_id = cate["cate_id"]
            weight = cate["weight"] + _weight + len(keyword.split(" "))
            if self.cateWeight.has_key(str(cate_id)):
                weight += self.cateWeight.get(str(cate_id))
            self.cateWeight[str(cate_id)] = weight
        return True

    def sortCateByWeight(self,cateWeights):
        if cateWeights == False or len(cateWeights) <1:
			return False
        #cateWeights = sorted(cateWeights.iteritems(), key = lambda asd:asd[1],reverse=True)

        cateWeights = sorted(cateWeights.iteritems(), key = lambda asd:asd[1],reverse=True)

        result = []
        for k,i in cateWeights:
            if i < 6:
                continue
            result.append(k)
        return result

    def findTopCate(self, cate_id=0):
        cate = DB.init().getOne('SELECT * FROM le_cate WHERE id=%s AND parent_id = 0 AND type ="goods"',[cate_id])
        if cate != False:
            return cate

        cate = DB.init().getOne('SELECT * FROM le_cate WHERE id=%s AND type ="goods"',[cate_id])
        if cate == False:
            return cate

        pid = cate['parent_id']
        if pid > 0:
            return self.findTopCate(pid)
        return cate

    def findByKeyword(self, keyword):
        sql = 'SELECT * FROM t_cate_keyword WHERE keyword like %s'
        inf = Inflector()
        fields = []
        fields.append(keyword)

        singularize = inf.singularize(keyword)
        if singularize != keyword:
            sql = sql + ' or keyword like %s'
            fields.append(singularize)

        pluralize = inf.pluralize(keyword)
        if pluralize != keyword:
            sql = sql + ' or keyword like %s'
            fields.append(pluralize)

        return DB.init().getAll(sql,fields)

if __name__ == "__main__":
    ds = SimpleClassifier()
    print ds.findCateAndTags('Burberry Checkered Necktie in Brown 3772316',4)
#!/usr/bin/python
#coding=utf-8
from base import *
import sys,os,time

reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb
'''
# class DB:
#     OBJECT = None
#     conn = None
#     cursor = None
#
#     def __init__(self):
#         self.connect()
#
#     @staticmethod
#     def init():
#         if DB.OBJECT == None:
#             DB.OBJECT = DB()
#         return DB.OBJECT
#
#
#     #self.conn = MySQLdb.connect(user='24a',db='test',passwd='24abcdef',host='localhost',unix_socket='/tmp/mysql.sock')#,unix_socket='/tmp/mysql.sock'
#     def connect(self):
#             print '==================='
#         # print self.db
#         # if self.db == 'sg':
#         #     self.conn = MySQLdb.connect(user='24a',db='ilovedeals',passwd='24abcdef',host='10.144.129.241',unix_socket='/tmp/mysql.sock')#,unix_socket='/tmp/mysql.sock'
#         # elif self.db == 'my':
#         #     self.conn = MySQLdb.connect(user='24a',db='myilovedeals',passwd='24abcdef',host='localhost',unix_socket='/tmp/mysql.sock')#,unix_socket='/tmp/mysql.sock'
#         # elif self.db == 'test':
#             self.conn = MySQLdb.connect(user = 'root',db='test',passwd = 'LEsc2008',host='localhost')
#
#     def execute(self, sql, args=None):
#         """
#
#         :rtype : object
#         """
#         try:
#             self.cursor = self.conn.cursor(cursorclass = MySQLdb . cursors . DictCursor)
#             self.cursor.execute('SET NAMES utf8')
#         except Exception, e:
#             print '---------------'+e.message
#             self.connect()
#             self.cursor = self.conn.cursor(cursorclass = MySQLdb . cursors . DictCursor)
#             self.cursor.execute('SET NAMES utf8')
#
#         try:
#             if args is not None:
#                 self.cursor.execute(sql,args)
#             else:
#                 self.cursor.execute(sql)
#             self.conn.commit()
#         except (AttributeError, MySQLdb.OperationalError):
#             print 'Mysql execute error'
#             logs('------ '+ time.strftime("%Y-%m-%d %H-%M-%S")+' Mysql execute error: '+sql)
#         return self.cursor
#
#
#     def close(self):
#         try:
#             if self.cursor:
#                 self.cursor.close()
#         except Exception, e:
#             print e.message+'---cursor'
#         try:
#             if self.conn:
#                 self.conn.close()
#         except Exception, e:
#             print e.message+'===conn'
#
#     def __del__(self):
#         self.close()
'''

"""
desc:数据库操作类
@note:
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理
"""
"""
Config是一些数据库的配置文件
"""

class DB(object):
    """
        MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现
        获取连接对象：conn = Mysql.getConn()
        释放连接对象;conn.close()或del conn
    """
    #连接池对象
    __pool = None
    __obj = None
    def __init__(self):
        """
        数据库构造函数，从连接池中取出连接，并生成操作游标
        """
#        self._conn = MySQLdb.connect(host=Config.DBHOST , port=Config.DBPORT , user=Config.DBUSER , passwd=Config.DBPWD ,
#                              db=Config.DBNAME,use_unicode=False,charset=Config.DBCHAR,cursorclass=DictCursor)
        self._conn = DB.__getConn()
        self._cursor = self._conn.cursor(cursorclass = MySQLdb . cursors . DictCursor)
        #self._cursor = self.conn.cursor(cursorclass = MySQLdb . cursors . DictCursor)
        self._cursor.execute('SET NAMES utf8')

    @staticmethod
    def init():
        if DB.__obj is None:
            DB.__obj = DB()

        return DB.__obj

    @staticmethod
    def __getConn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if DB.__pool is None:
                # if self.db == 'sg':
            #     self.conn = MySQLdb.connect(user='24a',db='ilovedeals',passwd='24abcdef',host='10.144.129.241',unix_socket='/tmp/mysql.sock')#,unix_socket='/tmp/mysql.sock'
            # elif self.db == 'my':
            #     self.conn = MySQLdb.connect(user='24a',db='myilovedeals',passwd='24abcdef',host='localhost',unix_socket='/tmp/mysql.sock')#,unix_socket='/tmp/mysql.sock'
            # elif self.db == 'test':
            try:
                DB.__pool = MySQLdb.connect(user = 'root',db='jisucms',passwd = 'LEsc2008',host='localhost',unix_socket='/tmp/mysql.sock')
            except Exception,e:
                DB.__pool = MySQLdb.connect(user = 'root',db='jisucms',passwd = 'LEsc2008',host='localhost')

        return DB.__pool

    def getAll(self,sql,param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """

        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        if count>0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    def getOne(self,sql,param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        if count>0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self,sql,num,param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        if count>0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertOne(self,sql,value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        try:
            self._cursor.execute(sql,value)
            return self.__getInsertId()
        except Exception, e:
            print e.message
            print self._cursor._last_executed

    def insertMany(self,sql,values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql,values)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self,sql,param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql,param)
        return count

    def update(self,sql,param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql,param)

    def delete(self,sql,param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql,param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self,option='commit'):
        """
        @summary: 结束事务
        """
        if option=='commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def __del__(self):
        self.dispose()

    def dispose(self,isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd==1:
            self.end('commit')
        else:
            self.end('rollback');
        self._cursor.close()
        self._conn.close()

if __name__ == '__main__':
    print 'ok'
#!/usr/bin/python
#coding=utf-8
'''
__author__ = 'ShengYue'
Email: ysc8620@163.com
'''

import sys,os
reload(sys)
sys.setdefaultencoding('utf8')

import hashlib,time

def get_simple_text(text):
    try:
        import re
        vocalMap = { 'a' : ['&agrave;','&aacute;','&acirc;','&atilde;','&auml;','&aring;','&aelig;','&#224;','&#225;','&#226;','&#227;','&#228;','&#229;','&#257;','&#230;'],
                     'e' : ['&egrave;','&eacute;','&ecirc;','&euml;','&#232;','&#233;','&#234;','&#235;','&#275;'],
                     'i' : ['&igrave;','&iacute;','&icirc;','&iuml;','&#236;','&#237;','&#238;','&#239;','&#299;'],
                     'o' : ['&ograve;','&oacute;','&ocirc;','&oelig;','&otilde;','&ouml;','&#242;','&#243;','&#244;','&#339;','&#245;','&#246;','&#333;'],
                     'u' : ['&ugrave;','&uacute;','&ucirc;','&uuml;','&#249;','&#250;','&#251;','&#252;','&#363;']
                    }

        text = text.strip()

        for vocale, lista in vocalMap.iteritems(): #per ogni elemento della mappa avrà una chiave ed una lista
            for elemento in lista: #itero su tutti gli elementi della lista
                text = text.replace(elemento,vocale) #sostituisco nel nome dell'offerta, la vocale all' HTML-entity

        text = text.replace("/","-")
        text = re.sub("[^a-zA-Z0-9_\s-]","",text)     #######################################
        text = re.sub("[\s-]+"," ",text)           #strippo tutti i caratteri non voluti:#
        text = re.sub("[\s_]","-",text)            #######################################
        text = re.sub("-+","-",text)
    except:
        pass
    return text

def get_title(text):
    text = get_simple_text(text)
    return text.lower()

def get_seo_title(str):
    str = get_title(str)
    str = (str if len(str)  > 2 else 'details') # len(str) < 2 ? str : 'details'
    return str.strip('-')

def logs(log):
    print log
    file("./error.log","a+").write(time.strftime("------%Y-%d-%d %H:%M:%S ") + " " +log+"\r")

def runlogs(log):
    print log
    file("./run.log","a+").write(time.strftime("------%Y-%d-%d %H:%M:%S ") + " " +log+"\r")

def urllogs(log):
    print log
    file("./url.log","a+").write(time.strftime("------%Y-%d-%d %H:%M:%S ") + " " +log+"\r")

def infourllogs(log):
    print log
    file("./infourl.log","a+").write(time.strftime("------%Y-%d-%d %H:%M:%S ") + " " +log+"\r")
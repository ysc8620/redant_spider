#!/bin/bash
killall -9 scrapy
basepath=$(cd `dirname $0`; pwd)
echo $basepath
cd $basepath
for file in `ls $basepath/kan360/websites/*.xml`
do
 name = $(basename "${file%%.*}")
 scrapy crawl dmoz -a name=$name
 sleep 1m
done
#scrapy crawl dmoz -a n=imobshop.xml > /soft/py.log
#sleep 5m
#scrapy crawl dmoz -a n=deal.com.sg.xml > /soft/deal.log
#sleep 5m
#scrapy crawl dmoz -a n=deal.com.my.xml > /soft/mydeal.log

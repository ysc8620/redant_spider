#!/bin/bash
killall -9 scrapy
basepath=$(cd `dirname $0`; pwd)
echo $basepath
cd $basepath
for file in `ls $basepath/kan360/websites/*.xml`
do
 echo $file
 n=$(basename "${file%%.*}")
 scrapy crawl dmoz -a name=$n
 #sleep 1m
done
#scrapy crawl dmoz -a n=imobshop.xml > /soft/py.log
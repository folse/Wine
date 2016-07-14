#/bin/bash  
arr=('http://www.systembolaget.se/dryck/roda-viner/7-deadly-zins-669001' 'http://www.systembolaget.se/dryck/roda-viner/a-1234302')
num=${#arr[@]}  
echo "$num item in array:"
for((i=0;i<num;i++));
do
 echo $i
 echo ${arr[i]}
 scrapy crawl wine -a url=${arr[i]}
 #sleep 5s
done
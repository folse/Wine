#/bin/bash  
arr=('file:///Users/folse/Downloads/Archive/scrapy_wine_store_id/stores.xml')
# arr=('http://www.systembolaget.se/api/assortment/stores/xml')
num=${#arr[@]}  
echo "$num item in array:"
for((i=0;i<num;i++));
do
 echo $i
 echo ${arr[i]}
 scrapy crawl wine -a url=${arr[i]}
 #sleep 5s
done
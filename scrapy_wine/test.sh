#/bin/bash
# arr=('/dryck/roda-viner/7-deadly-zins-669001' '/dryck/roda-viner/a-1234302' '/dryck/roda-viner/a-1234301' '/dryck/roda-viner/a-quo-9256001' '/dryck/roda-viner/adobe-629808' '/dryck/roda-viner/adobe-685301' '/dryck/roda-viner/aglianico-del-vulture-463401' '/dryck/roda-viner/alamos-667001' '/dryck/roda-viner/albret-601401' '/dryck/roda-viner/allegrini-230908' '/dryck/roda-viner/allegrini-7499701' '/dryck/roda-viner/allegrini-601001')
arr=('/dryck/roda-viner/7-deadly-zins-669001')
num=${#arr[@]}
echo "$num item in array:"
for((i=0;i<num;i++));
do
 echo $i
 echo ${arr[i]}
 scrapy crawl wine -a url='http://www.systembolaget.se'${arr[i]}
 #sleep 5s
done
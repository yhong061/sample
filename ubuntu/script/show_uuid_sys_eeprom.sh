#!/bin/bash

offset=0x116
line='0000116'
num=16
binfile='/tmp/fru.bin'

cmd=$(ipmitool fru read 0 ${binfile})
uuid_str=$(hexdump -s ${offset} -n ${num} -C ${binfile} | \
grep ${line} | awk '{for (i=2;i<($num)+2;i++) print $i " ";}')

arr=($(echo $uuid_str | tr " " "\n"))
echo "UUID: " ${arr[3]^^}${arr[2]^^}${arr[1]^^}${arr[0]^^}"-"\
${arr[5]^^}${arr[4]^^}"-"${arr[7]^^}${arr[6]^^}"-"${arr[8]^^}${arr[9]^^}"-"\
${arr[10]^^}${arr[11]^^}${arr[12]^^}${arr[13]^^}${arr[14]^^}${arr[15]^^}

rm ${binfile}
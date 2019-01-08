#!/bin/sh

#--------------------------------------
#awk参数说明:
# $0 for the whole line.
# $1 for the first field.
# $2 for the second field.
# $n for the nth field.

echo "Hello Tom" | awk '{$2="Adam"; print $0}'
# $0: Hello Tom
# $1: Hello
# $2: Tom

# -F fs     To specify a file separator.
# -f file     To specify a file that contains awk script.
# -v var=value     To declare a variable.

#--------------------------------------
# awk语句格式说明:
# format: awk options program file
#         awk '{print $1}' /etc/passwd      //执行print $1语句， 默认以'space'作为分隔符
#         awk -F: '{print $1}' /etc/passwd  //执行print $1语句， -F替换分隔符，以':'作为分隔符
#         awk -F: script_file /etc/passwd   //script_file文件中地语句，以':'作为分隔符
#           script_file文件中地语句格式: {print $1}

#--------------------------------------
# BEGIN and END keywords:
# BEGIN: You can use the BEGIN keyword to run a script before processing the data
# END  : To run a script after processing the data, use the END keyword
# Example: 
    # awk 'BEGIN {print "The File Contents:"}
    # {print $0}
    # END {print "File footer"}' myfile

#--------------------------------------
# awk语句高级用法
# FIELDWIDTHS     Specifies the field width.
# RS     Specifies the record separator.
# FS     Specifies the field separator.
# OFS  Specifies the Output separator.
# ORS  Specifies the Output separator.

awk 'BEGIN{FIELDWIDTHS="3 4 3"}{print $1,$2,$3}' testfile   #将testfile地内容按执行字符宽度分割
awk 'BEGIN{FS=":"; OFS="-"} {print $1,$6,$7}' /etc/passwd   #将passwd中地":"换成"-"





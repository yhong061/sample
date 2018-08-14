#/bin/sh

# $( ) 与 ` ` (反引号) :命令
# $var == ${var}       :变量
# A=(a b c  def)       :数组
# $(( ))               :整数运算

# $# :总的参数数目
# $n :第几个参数，$1 表示第一个参数，$2 表示第二个参数 ... 　　
# $0 :当前程序的名称
# $* :所有参数组成的字符串
# $@ :以"参数1" "参数2" ... 形式保存所有参数

# '' : 防止任何变量扩展
# "" : 防止通配符扩展但允许变量扩展

#---------------$# #n $@ $$ $?: para
#./shell.sh i j k m
if [ "$1" == "para" ]; then
echo $# #参数个数: 4
echo $0 #第0个参数: ./shell.sh
echo $1 #第一个参数: i
echo $@ #所有参数的列表(以一个单字符串显示所有参数)
echo $* #所有参数的列表(以一个单字符串显示所有参数)
echo $$ #当前进程ID
echo $? #显示执行上一条Shell命令的返回值，0表示没有错误
fi

#---------------$"var" 'var'
if [ "$1" == "other" ]; then
echo $SHELL   # => /bin/bash
echo "$SHELL" # => /bin/bash
echo '$SHELL' # => $SHELL
fi

#---------------$(): 命令
if [ "$1" == "cmd" ]; then
echo the last sunday is $(date -d "last sunday" +%Y-%m-%d)
fi

#---------------${}: 变量
if [ "$1" == "var" ]; then
file=dir0/dir1/dir2/dir3/my.file.txt
# '#' 在 '$' 左边, '%' 在 '$' 右边
echo ${file#*/}  #拿掉 字符'/' 左边 的字符串(  第一次出现) ：dir1/dir2/dir3/my.file.txt
echo ${file##*/} #拿掉 字符'/' 左边 的字符串(最后一次出现) ：my.file.txt
echo ${file%/*}  #拿掉 字符'/' 右边 的字符串(最后一次出现) ：dir0/dir1/dir2/dir3
echo ${file%%/*} #拿掉 字符'/' 右边 的字符串(  第一次出现) ：dir0
echo ${file:5:5} #提取第 5 个字节右边的连续 5 个字节：dir1/

echo ${file/dir/path}  #将第一个 dir 提换为 path：/path0/dir1/dir2/dir3/my.file.txt
echo ${file//dir/path} #将  全部 dir 提换为 path：/path0/path1/path2/path3/my.file.txt
echo ${#file}          #计算变量值的长度: 31
fi

#---------------A=() 数组
if [ "$1" == "array" ]; then
B="a b c def" #$B 替换为一个单一的字符串，
A=(a b c def) #$A 定义为组数

echo ${B}     #可得到 "a b c def" (字符串)
echo ${A[@]}  #可得到 a b c def (全部组数)
echo ${A[*]}  #可得到 a b c def (全部组数)
echo ${A[0]}  #可得到 a (第一个组数)，${A[1]} 则为第二个组数…
echo ${#A[@]} #可得到 4 (全部组数数量)
echo ${#A[*]} #可得到 4 (全部组数数量)
echo ${#A[0]} #可得到 1 (即第一个组数(a)的长度)
A[3]=xyz      #将第四个组数重新定义为 xyz …
echo ${A[@]}  #可得到 a b c xyz (全部组数)
fi

#---------------$(()) : 整数运算
if [ "$1" == "calc" ]; then
a=5; b=7; c=2
echo $(( a+b*c ))   #19
echo $(( (a+b)/c )) #6
echo $(( (a*b)%c))  #1
fi

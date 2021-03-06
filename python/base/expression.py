#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\d 可以匹配一个数字，\w 可以匹配一个字母或数字:
	'00\d'可以匹配'007'，但无法匹配'00A'；
	'\d\d\d'可以匹配'010'；
	'\w\w\d'可以匹配'py3'；

. 可以匹配任意字符，所以：
	'py.'可以匹配'pyc'、'pyo'、'py!'等等。

* 表示任意个字符（包括0个）， + 表示至少一个字符， ? 表示0个或1个字符， {n} 表示n个字符， {n,m} 表示n-m个字符：

\d{3}\s+\d{3,8}: 可以匹配以任意个空格隔开的带区号的电话号码
	\d{3}表示匹配3个数字，例如'010'；
	\s可以匹配一个空格（也包括Tab等空白符），所以\s+表示至少有一个空格，例如匹配' '，' '等；
	\d{3,8}表示3-8个数字，例如'1234567'。

如果要匹配'010-12345'这样的号码呢？由于'-'是特殊字符，在正则表达式中，要用'\'转义，所以，上面的正则是\d{3}\-\d{3,8}。


[] 表示范围: 
	[0-9a-zA-Z\_]可以匹配一个数字、字母或者下划线；
	[0-9a-zA-Z\_]+可以匹配至少由一个数字、字母或者下划线组成的字符串，比如'a100'，'0_Z'，'Py3000'等等；
	[a-zA-Z\_][0-9a-zA-Z\_]*可以匹配由字母或下划线开头，后接任意个由一个数字、字母或者下划线组成的字符串，也就是Python合法的变量；
	[a-zA-Z\_][0-9a-zA-Z\_]{0, 19}更精确地限制了变量的长度是1-20个字符（前面1个字符+后面最多19个字符）。

A|B 可以匹配A或B，所以(P|p)ython可以匹配'Python'或者'python'。

^ 表示行的开头，^\d表示必须以数字开头。
$ 表示行的结束，\d$表示必须以数字结束。

#============================
#============================
re模块

s = 'ABC\\-001' # Python的字符串
# 'ABC\-001'

#使用Python的r前缀，就不用考虑转义的问题了
s = r'ABC\-001' # Python的字符串
# 'ABC\-001'

#match()方法判断是否匹配，如果匹配成功，返回一个Match对象，否则返回None。
import re
re.match(r'^\d{3}\-\d{3,8}$', '010-12345')
#<_sre.SRE_Match object; span=(0, 9), match='010-12345'>

#============================
#============================
切分字符串: re.split

re.split(r'\s+', 'a b   c')
#['a', 'b', 'c']
无论多少个空格都可以正常分割。加入,试试：

re.split(r'[\s\,]+', 'a,b, c  d')
#['a', 'b', 'c', 'd']

re.split(r'[\s\,\;]+', 'a,b;; c  d')
#['a', 'b', 'c', 'd']
#============================
#============================
分组: ()表示的就是要提取的分组（Group）。比如：

^(\d{3})-(\d{3,8})$分别定义了两个组，可以直接从匹配的字符串中提取出区号和本地号码：

m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
m.group(0)
#'010-12345'
m.group(1)
#'010'
m.group(2)
#'12345'

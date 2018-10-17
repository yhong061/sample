#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print('====list[]====')
print('====tuple()====')
print('====Dict{key : value}====')
print('====Set([key])====')
print('====Slice: List[::]====')
print('====迭代 for i in L====')
print('====列表生成式: x * x for x in range(10)====')
print('====generator: List[], generator()====')
print('====Iterable/Iterator====')


#============================
# list是一种有序的集合，可以随时添加和删除, 替换其中的元素
# 和Dict比，优点:
#     查找和插入的时间随着元素的增加而增加；
#     占用空间小，浪费内存很少。
# 最后一个元素，除了计算索引位置外，还可以用-1做索引
# len() : 获得list元素的个数
# insert() : 插入
# append() : 追加
# pop() : 删除
# sort() : 排序
#============================
print('====list[]====')

classmates = ['Michael', 'Bob', 'Tracy']
print(classmates)       #['Michael', 'Bob', 'Tracy']
print(len(classmates))  #3
print(classmates[0])    #'Michael'
print(classmates[2])    #'Tracy'

print(classmates[-1])   #'Tracy'
print(classmates[-3])   #'Michael'

classmates.insert(1, 'Jack')
print(classmates)       #['Michael', 'Jack', 'Bob', 'Tracy']

classmates.append('Adam')
print(classmates)       #['Michael', 'Jack', 'Bob', 'Tracy', 'Adam']

classmates.pop()
print(classmates)       #['Michael', 'Jack', 'Bob', 'Tracy']
classmates.pop(1)
print(classmates)       #['Michael', 'Bob', 'Tracy']

classmates[1] = 'Sarah'
classmates.sort()
print(classmates)       #['Michael', 'Sarah', 'Tracy']



# list里面的元素的数据类型也可以不同
L = ['Apple', 123, True]

# list元素也可以是另一个list
s = ['python', 'java', ['asp', 'php'], 'scheme']
print(len(s))         #4
print(s[2][1])        #php

# 空的list，它的长度为0
L = []

#============================
# 另一种有序列表叫元组：tuple
# tuple一旦初始化就不能修改
#============================
print('====tuple()====')

classmates = ('Michael', 'Bob', 'Tracy')

print(classmates)       #('Michael', 'Bob', 'Tracy')
print(len(classmates))  #3
print(classmates[0])    #'Michael'
print(classmates[2])    #'Tracy'

print(classmates[-1])   #'Tracy'
print(classmates[-3])   #'Michael'

# 只有1个元素的tuple, 必须加一个逗号，来消除歧义
t = (1,)

#============================
# Dict : 使用键-值（key-value）存储
# 和list比，优点:
#    查找和插入的速度极快，不会随着key的增加而变慢；
#    需要占用大量的内存，内存浪费多。
# get()，如果key不存在，可以返回None
# pop(): 删除一个key
#============================
print('====Dict{key : value}====')

d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d['Michael'])   #95

d['Adam'] = 67
print(d['Adam'])     #67

# in判断key是否存在
print('Thomas' in d)         #False
print(d.get('Thomas'))       #None
print(d.get('Thomas', -1))   #-1

print(d.pop('Bob'))   #75
print(d)              #{'Michael': 95, 'Tracy': 85, 'Adam': 67}


#============================
# set和dict类似，但不存储value, key不能重复
# add() : 添加
# remove(): 删除
#============================
print('====Set([key])====')

s = set([1, 2, 3])
print(s)   #s = set([1, 2, 3])
s = set([1, 1, 2, 2, 3, 3])
print(s)   #s = set([1, 2, 3])

print(s.add(4))
print(s)   #s = set([1, 2, 3, 4])

print(s.remove(3))
print(s)   #s = set([1, 2, 4])

print(s.add(3))
print(s)   #s = set([1, 2, 3, 4])

#============================
# Slice 操作符
#tuple也是一种list，也可以用切片操作，只是操作的结果仍是tuple
#字符串'xxx'也可以看成是一种list，也可以用切片操作，只是操作结果仍是字符串
#============================
print('====Slice: List[::]====')

L = list(range(100))
print(L)        #[0, 1, 2, 3, ..., 99]
print(L[:5])    #前5个数 [0, 1, 2, 3, 4]
print(L[-5:])   #后5个数 [95, 96, 97, 98, 99]
print(L[10:15]) #前11-15个数 [10, 11, 12, 13, 14]
print(L[:10:2]) #前10个数，每两个取一个[0, 2, 4, 6, 8]
print(L[::20])  #所有数，每20个取一个 [0, 20, 40, 60, 80]

print('ABCDEFG'[:3])   #'ABC'
print('ABCDEFG'[::2])  #'ACEG'

#============================
#通过for循环来遍历这个list或tuple，这种遍历我们称为迭代（Iteration）
#迭代是通过for ... in来完成的
#
#isinstance() 判断一个对象是可迭代对象
#enumerate()  把一个list变成[索引-元素]
#============================
print('====迭代 for i in L====')

#Dict: 
#默认迭代的是key， for key in d
#如果要迭代value，可以用for value in d.values()
#如果要同时迭代key和value，可以用for k, v in d.items()
#dict的存储不是按照list的方式顺序排列，所以，迭代出的结果顺序很可能不一样
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)

#字符串也是可迭代对象
for ch in 'ABC':
    print(ch)

#判断一个对象是可迭代对象, 通过collections模块的Iterable类型
from collections import Iterable    
print(isinstance('abc', Iterable))   #True
print(isinstance([1,2,3], Iterable)) #True
print(isinstance(123, Iterable))     #False

#Python内置的enumerate函数可以把一个list变成[索引-元素]
for i, value in enumerate(['A', 'B', 'C']):
    print(i, value)
#/* 
# * 0 A
# * 1 B
# * 2 C
# */
#============================
#列表生成式
#============================
print('====列表生成式: x * x for x in range(10)====')

#生成[1x1, 2x2, 3x3, ..., 10x10]
#写列表生成式时，把要生成的元素x * x放到前面，后面跟for循环
print([x * x for x in range(1, 11)]) #[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    
#for循环后面还可以加上if判断
print([x * x for x in range(1, 11) if x % 2 == 0]) #[4, 16, 36, 64, 100]

#还可以使用两层循环，可以生成全排列：
print([m + n for m in 'ABC' for n in 'XYZ'])
#['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']

#列出当前目录下的所有文件和目录名
import os
print([d for d in os.listdir('.')])
#['readme.txt', 'function.py', 'module.py']

#列表生成式也可以使用两个变量来生成list
d = {'x': 'A', 'y': 'B', 'z': 'C' }
print([k + '=' + v for k, v in d.items()]) #['x=A', 'y=B', 'z=C']

#把一个list中所有的字符串变成小写
L = ['Hello', 'World', 'IBM', 'Apple']
print([s.lower() for s in L]) #['hello', 'world', 'ibm', 'apple']


#============================
#在Python中，这种一边循环一边计算的机制，称为生成器：generator。
#yield语句: 遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行
#============================
print('====generator: List[], generator()====')

#L和g的区别仅在于最外层的[]和()，L是一个list，而g是一个generator
L = [x * x for x in range(10)]  #list
print(L)
g = (x * x for x in range(10))  #generator
print(g)

#使用for循环, 获得generator的返回值
for n in g:
    print(n)

#generator和函数的执行流程不一样。
#函数是顺序执行，遇到return语句或者最后一行函数语句就返回。
#而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行
        
#fib: 斐波拉契数列, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a + b
        n = n + 1
    return 'done'   

#把fib函数变成generator，只需要把print(b)改为yield b就可以了
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'

f=fib(6)  #generator
print(f)

#============================
# 迭代器:
#1. 可以直接作用于for循环的对象统称为可迭代对象： Iterable(可迭代对象)
#   一类是集合数据类型，如list、tuple、dict、set、str等；
#   一类是generator，包括生成器和带yield的generator function。
#   可以使用isinstance()判断一个对象是否是Iterable对象

#2. 可以被next()函数调用并不断返回下一个值的对象称为迭代器： Iterator(迭代器)
#   可以使用isinstance()判断一个对象是否是Iterator对象

#Python的Iterator对象表示的是一个数据流，Iterator对象可以被next()函数调用并不断
#返回下一个数据，直到没有数据时抛出StopIteration错误。可以把这个数据流看做是一个有序
#序列，但我们却不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据，所
#以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算。
#============================
print('====Iterable/Iterator====')

from collections import Iterable
print(isinstance([], Iterable))                     #True
print(isinstance({}, Iterable))                     #True
print(isinstance('abc', Iterable))                  #True
print(isinstance((x for x in range(10)), Iterable)) #True
print(isinstance(100, Iterable))                    #False


from collections import Iterator
print(isinstance([], Iterator))                     #False
print(isinstance({}, Iterator))                     #False
print(isinstance('abc', Iterator))                  #False
print(isinstance((x for x in range(10)), Iterator)) #True
print(isinstance(100, Iterator))                    #False

#generator都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator
#把list、dict、str等Iterable变成Iterator可以使用iter()函数

print(isinstance(iter([]), Iterator))               #True
print(isinstance(iter('abc'), Iterator))            #True


#============================
#枚举类型定义一个class类型，然后，每个常量都是class的一个唯一实例。
#============================
print('====Enum====')

#1. Python提供了Enum类来实现这个功能： 

from enum import Enum

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value) #value属性则是自动赋给成员的int常量，默认从1开始计数。
#Jan => Month.Jan , 1

#2. 从Enum派生出自定义类：
from enum import Enum, unique

@unique
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

day1 = Weekday.Mon
print(day1)
#Weekday.Mon
print(Weekday.Tue)
#Weekday.Tue
print(Weekday['Tue'])
#Weekday.Tue
print(Weekday.Tue.value)
#2
print(day1 == Weekday.Mon)
#True
print(day1 == Weekday.Tue)
#False
print(Weekday(1))
#Weekday.Mon
for name, member in Weekday.__members__.items():
    print(name, '=>', member)

#Sun => Weekday.Sun
#Mon => Weekday.Mon
#Tue => Weekday.Tue
#Wed => Weekday.Wed
#Thu => Weekday.Thu
#Fri => Weekday.Fri
#Sat => Weekday.Sat


#============================
#============================

#============================
#============================

#============================
#============================

#============================
#============================

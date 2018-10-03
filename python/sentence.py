#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#============================
# 条件判断:
# 注意不要少写了冒号:
#============================
print('====条件语句====')

s = input('input your age : ') 
age = int(s)
if age >= 60:
    print('your age is', age)
    print('old')
elif age >=18:
    print('your age is', age)
    print('adult')
else:
    print('your age is', age)
    print('teenager')


#============================
# 循环语句
# 1. for...in循环 
# 2. while
#
# break, continue
#============================

print('====循环语句====')
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)

# 计算0-100的整数序列
sum = 0
for x in range(101):
    sum = sum + x
print(sum)

# 计算100以内所有奇数之和
sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)



#============================
#============================
#============================
#============================
#============================
#============================

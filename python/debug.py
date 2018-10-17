#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Python所有的错误都是从BaseException类派生的，常见的错误类型和继承关系看这里：
#https://docs.python.org/3/library/exceptions.html#exception-hierarchy

#raise语句抛出一个错误的实例
#Python内置的logging模块可以非常容易地记录错误信息

#============================
#try的机制
#============================
print('====try...except...finally====')
#如果执行出错，则后续代码不会继续执行，而是直接跳转至错误处理代码，即except语句块，
#执行完except后，如果有finally语句块，则执行finally语句块，至此，执行完毕。
#try...
#except: division by zero
#finally...
#END

#没有错误发生，except语句块不会被执行，但是finally如果有，则一定会被执行
#try...
#result: 5
#finally...
#END

try:
    print('try...')
    r = 10 / 0
    print('result:', r)
except ZeroDivisionError as e:
    print('except:', e)
finally:
    print('finally...')
print('END')

#如果发生了不同类型的错误，应该由不同的except语句块处理。
#如果没有错误发生，会自动执行else语句
try:
    print('try...')
    r = 10 / int('2')
    print('result:', r)
except ValueError as e:
    print('ValueError:', e)
except ZeroDivisionError as e:
    print('ZeroDivisionError:', e)
else:
    print('no error!')
finally:
    print('finally...')
print('END')

#============================
#调试：
#============================

#如果要比较爽地设置断点、单步执行，就需要一个支持调试功能的IDE。目前比较好的Python IDE有：
#Visual Studio Code：https://code.visualstudio.com/，需要安装Python插件。
#PyCharm：http://www.jetbrains.com/pycharm/
#另外，Eclipse加上pydev插件也可以调试Python程序。

#1. print() 打印

#2. assert  断言
#assert n != 0, 'n is zero!'
#启动Python解释器时可以用-O参数来关闭assert

#3. logging不会抛出错误，而且可以输出到文件
#有debug，info，warning，error等几个级别

import logging
logging.basicConfig(level=logging.INFO)

s = '0'
n = int(s)
logging.info('n = %d' % n)
print(10 / n)

#4. Python的调试器pdb
#python -m pdb err.py
#命令l来查看代码
#命令n可以单步执行代码
#命令p 变量名来查看变量
#命令q结束调试

#5. pdb.set_trace()
import pdb

s = '0'
n = int(s)
pdb.set_trace() # 运行到这里会自动暂停
print(10 / n)

#============================
#============================


#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#============================
#file-like Object
#像open()函数返回的这种有个read()方法的对象，在Python中统称为file-like Object
#StringIO就是在内存中创建的file-like Object，常用作临时缓冲
#============================


#============================
#读文件
#如果文件不存在，open()函数就会抛出一个IOError的错误
#文件读写时都有可能产生IOError
#遇到有些编码不规范的文件，你可能会遇到UnicodeDecodeError
#============================

#法一
#f = open('/home/yhong/sample/test.txt', 'r')  #读取UTF-8编码的文本文件
#f = open('/home/yhong/sample/test.jpg', 'rb') #读取二进制文件
#f = open('/home/yhong/sample/gbk.txt', 'r', encoding='gbk') #读取GBK编码的文件
#f = open('/home/yhong/sample/gbk.txt', 'r', encoding='gbk', errors='ignore') #errors参数，表示如果遇到编码错误后如何处理
#f.read() 	  #一次读取文件的全部内容
#f.read(size)  #最多读取size个字节的内容
#f.readline()  #可以每次读取一行内容，
#f.readlines() #一次读取所有内容并按行返回list
#f.close()

#for line in f.readlines():
#    print(line.strip()) # 把末尾的'\n'删掉

#法二： 使用try ... finally
try:
    f = open('/home/yhong/sample/sample/python/test', 'r')
    print(f.read())
finally:
    if f:
        f.close()

#法三： with语句来自动帮我们调用close()方法	
with open('/home/yhong/sample/sample/python/test', 'r') as f:
    print(f.read())



#============================
#写文件
#当我们写文件时，操作系统往往不会立刻把数据写入磁盘，而是放到内存缓存起来，空闲的时候再慢慢写入。只有调用close()方法时，操作系统才保证把没有写入的数据全部写入磁盘。
#============================

f = open('/home/yhong/sample/sample/python/test', 'w')
f.write('Hello, world!')
f.close()

with open('/home/yhong/sample/sample/python/test', 'w') as f:
    f.write('Hello, world!')


#============================
#StringIO： 在内存中读写str
#============================

print('====StringIO：====')
from io import StringIO
f = StringIO()   #创建一个StringIO
f.write('hello')
f.write(' ')
f.write('world!')
print(f.getvalue())

f = StringIO('Hello!\nHi!\nGoodbye!')
while True:
	s = f.readline()
	if s == '':
		break
	print(s.strip())

#============================
#BytesIO: 操作二进制数据
#============================

print('====BytesIO====')
from io import BytesIO
f = BytesIO()
f.write('中文'.encode('utf-8'))  #写入的不是str，而是经过UTF-8编码的bytes
print(f.getvalue())	
	
f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
f.read()
	

#============================
#操作文件和目录
#============================
#Python内置的os模块也可以直接调用操作系统提供的接口函数
#shutil模块提供了copyfile()的函数，你还可以在shutil模块中找到很多实用函数

print('====File and Dir====')
import os
os.name     #操作系统类型
os.uname()  #获取详细的系统信息
os.environ  #环境变量
os.environ.get('PATH')  #环境变量PATH

os.path.abspath('.')  #查看当前目录的绝对路径
os.mkdir('/home/yhong/sample/testdir')  #然后创建一个目录:
os.rmdir('/home/yhong/sample/testdir') #删掉一个目录

os.path.join('/Users/michael', 'testdir') #在某个目录下创建一个新目录，首先把新目录的完整路径表示出来
#'/home/yhong/sample/testdir'

os.path.split('/home/yhong/sample/testdir/file.txt') #拆分路径
#('/home/yhong/sample/testdir', 'file.txt')

os.path.splitext('/path/to/file.txt')  #得到文件扩展名
#('/path/to/file', '.txt')

os.rename('test.txt', 'test.py')  # 对文件重命名:
os.remove('test.py')  # 删掉文件:

#os.path.join()返回这样的字符串：
#在Linux/Unix/Mac： part-1/part-2
#在Windows       ： part-1\part-2

#列出当前目录下的所有目录：
[x for x in os.listdir('.') if os.path.isdir(x)]
#['.lein', '.local', '.m2', '.npm', '.ssh', '.Trash', '.vim', 'Applications', 'Desktop', ...]

#列出所有的.py文件：
[x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
['apis.py', 'config.py', 'models.py', 'pymonitor.py', 'test_db.py', 'urls.py', 'wsgiapp.py']

#============================
#序列化
#把变量从内存中变成可存储或传输的过程称之为序列化，在Python中叫pickling
#把变量内容从序列化的对象重新读到内存里称之为反序列化，即unpickling。
#Python提供了pickle模块来实现序列化。
#============================

#pickle.dumps(): 把任意对象序列化成一个bytes
import pickle
d = dict(name='Bob', age=20, score=88)
pickle.dumps(d)    

#pickle.dump(): 对象序列化后写入一个file-like Object
f = open('dump.txt', 'wb')
pickle.dump(d, f)  
f.close()

#pickle.load(): 从一个file-like Object中直接反序列化出对象
f = open('dump.txt', 'rb')
d = pickle.load(f) 
f.close()
print('d: ', d)

#============================
#JSON
#https://docs.python.org/3/library/json.html#json.dumps
#JSON表示的对象就是标准的JavaScript语言的对象，JSON和Python内置的数据类型对应如下：
#----------------------
#JSON类型       Python类型
#----------------------
#{}	        dict
#[]	        list
#"string"	str
#1234.56        int或float
#true/false	True/False
#null	        None
#----------------------
#============================

#dumps()方法返回一个str
#dump()方法可以直接把JSON写入一个file-like Object
import json
d = dict(name='Bob', age=20, score=88)
json.dumps(d)  

#loads(): 把JSON的字符串反序列化，
#load(): 从file-like Object中读取字符串并反序列化
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
json.loads(json_str)

#============================
#============================

		
#============================
#============================

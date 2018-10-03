#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#http://docs.python.org/3/library/functions.html

#help([object])
#help(abs)

#abs(x) 
#bin(x)
#chr(i)
#divmod(a, b)
#hex(x)
#len(s)
#oct(x)
#ord(c)
#
#all(iterable)
#any(iterable)
#enumerate(iterable, start=0)
#next(iterator[, default])
#sorted(iterable, *, key=None, reverse=False)
#sum(iterable[, start])
#tuple([iterable])
#zip(*iterables)
#
#filter(function, iterable)
#map(function, iterable, ...)
#
#ascii(object)
#repr(object)
#callable(object)
#dir([object])
#delattr(object, name)  
#exec(object[, globals[, locals]])
#getattr(object, name[, default])
#hasattr(object, name)
#hash(object)
#id(object)
#isinstance(object, classinfo)  #数据类型检查
#iter(object[, sentinel])
#setattr(object, name, value)
#vars([object])
#
#class object
#class bytearray([source[, encoding[, errors]]])       
#class bool([x])
#class bytes([source[, encoding[, errors]]])
#class complex([real[, imag]])
#class float([x])
#class frozenset([iterable])
#class dict(**kwarg)
#class dict(mapping, **kwarg)
#class dict(iterable, **kwarg)
#class int([x])
#class int(x, base=10)
#class list([iterable])
#class property(fget=None, fset=None, fdel=None, doc=None)
#class set([iterable])
#class slice(stop)
#class slice(start, stop[, step])
#class str(object='')
#class str(object=b'', encoding='utf-8', errors='strict')
#class type(object)
#class type(name, bases, dict)
#issubclass(class, classinfo)
#
#breakpoint(*args, **kws)
#
#compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)
#
#max(iterable, *[, key, default])
#max(arg1, arg2, *args[, key])
#min(iterable, *[, key, default])
#min(arg1, arg2, *args[, key])
#range(stop)
#range(start, stop[, step])
#round(number[, ndigits])¶
#pow(x, y[, z])
#
#eval(expression, globals=None, locals=None)
#format(value[, format_spec])
#
#input([prompt])
#memoryview(obj)
#
#open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)¶
#print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
#reversed(seq)
#super([type[, object-or-type]])
#
#@classmethod()         
#@staticmethod()
#   
#globals()
#locals()
#
#__import__(name, globals=None, locals=None, fromlist=(), level=0)


#============================
# 定义一个函数要使用def语句, 冒号结尾:。
# 其他文件引用可以使用from (filename) import my_abs来导入my_abs()函数
#============================
def my_abs(x):
    # 只允许整数和浮点数类型的参数
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x

#============================
# 空函数，可以用pass语句
#============================
def nop():
    pass

#============================
# 返回多个值
# 返回值是一个tuple
#============================
import math

def move(x, y, step, angle=0):
   nx = x + step * math.cos(angle)
   ny = y - step * math.sin(angle)
   return nx, ny

x, y = move(100, 100, 60, math.pi / 6)
print(x, y)   #(151.96152422706632, 70.0)

#============================
# 默认参数
#============================
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s

print(power(5))     #25
print(power(5, 3))  #125

#============================
# 默认参数
#============================
def enroll(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)

print(enroll('Bob', 'M', 7))
print(enroll('Adam', 'M', city='Tianjin'))


#============================
# 默认参数对可变参数地影响
#============================
def add_end(L=[]):
    L.append('END')
    return L

print(add_end()) # ['END']
print(add_end()) # ['END', 'END']

def add_end2(L=None):
    if L is None:
        L = []
    L.append('END')
    return L

print(add_end2()) # ['END']
print(add_end2()) # ['END']

#============================
# 可变参数: *list
#============================

# list , tuple 参数
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

print(calc([1, 2, 3]))    #list参数
print(calc((1, 3, 5, 7))) #tuple参数

# 可变参数
def calc2(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

print(calc2(1, 2))
print(calc2(1, 2, 3))
nums = [1, 2, 3]
calc2(*nums)    #*nums表示把nums这个list的所有元素作为可变参数传进去

#============================
# 关键字参数: **Dict
#============================
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

print(person('Bob', 35, city='Beijing'))
    #('name:', 'Bob', 'age:', 35, 'other:', {'city': 'Beijing'})
print(person('Adam', 45, gender='M', job='Engineer'))
    #('name:', 'Adam', 'age:', 45, 'other:', {'gender': 'M', 'job': 'Engineer'})

extra = {'city': 'Beijing', 'job': 'Engineer'}
print(person('Jack', 24, **extra))
    #('name:', 'Jack', 'age:', 24, 'other:', {'city': 'Beijing', 'job': 'Engineer'})


#============================
# 命名关键字参数: *, para, para, ...  (python3.7 support)
# 命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数
#============================
def person(name, age, *args, city='Beijing', job):
    print(name, age, city, job)

print(person('Jack', 24,  job='Engineer'))

def person2(name, age, *, city='Beijing', job):
    print(name, age, city, job)

print(person2('Jack', 24,  job='Engineer'))

#============================
#map() && reduce()
#map()函数接收两个参数，一个是函数，一个是Iterable，
#map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回。
#由于结果r是一个Iterator，Iterator是惰性序列，
#因此通过list()函数让它把整个序列都计算出来并返回一个list。
#
#reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，
#reduce把结果继续和序列的下一个元素做累积计算
#============================
print('=====map/reduce====')
#map(function, iterable, ...)
def f(x):
        return x * x

r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
print('map:', list(r))
#map: [1, 4, 9, 16, 25, 36, 49, 64, 81]

#数字转为字符串
print('int2str: ', list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9])))
#int2str:  ['1', '2', '3', '4', '5', '6', '7', '8', '9']

#reduce(function, iterable, ...)
from functools import reduce
def fn(x, y):
    return x * 10 + y

print('reduce', reduce(fn, [1, 3, 5, 7, 9]))  #13579 

#把str转换为int的函数
from functools import reduce

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return DIGITS[s]
    return reduce(fn, map(char2num, s))

print('str2int:', str2int('54321'))  #str2int: 54321

#============================
#filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素
#============================
print('=====filter====')
#在一个list中，删掉偶数，只保留奇数
def is_odd(n):
   return n % 2 == 1

print('filter:', list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])))
#filter: [1, 5, 9, 15]

#把一个序列中的空字符串删掉
def not_empty(s):
    return s and s.strip()

print('filter:', list(filter(not_empty, ['A', '', 'B', None, 'C', '  '])))
#filter: ['A', 'B', 'C']


#============================
#sorted()函数就可以对list进行排序：
#============================
print('====sorted====')
print('sorted: ', sorted([36, 5, -12, 9, -21]))
#sorted:  [-21, -12, 5, 9, 36]

#按绝对值大小排序
sorted([36, 5, -12, 9, -21], key=abs)

print('sorted: ', sorted(['bob', 'about', 'Zoo', 'Credit']))
#sorted:  ['Credit', 'Zoo', 'about', 'bob']
##忽略大小写的排序
print('sorted: ', sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower))
#sorted:  ['about', 'bob', 'Credit', 'Zoo']
#反向排序
print('sorted: ', sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True))
#sorted:  ['Zoo', 'Credit', 'bob', 'about']


#============================
#函数作为返回值
#============================
print('====函数作为返回值====')
#当我们调用lazy_sum()时，返回的并不是求和结果，而是求和函数
#内部函数sum可以引用外部函数lazy_sum的参数和局部变量，
#当lazy_sum返回函数sum时，相关参数和变量都保存在返回的函数

def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
           ax = ax + n
        return ax
    return sum    #函数作为返回值

f = lazy_sum(1, 3, 5, 7, 9)
print('f = ', f)     #f =  <function lazy_sum.<locals>.sum at 0x7f32f8f17ea0>
print('f() = ', f()) #f() =  25
                                                    
f1 = lazy_sum(1, 3, 5, 7, 9)
f2 = lazy_sum(1, 3, 5, 7, 9)    
print('f1 == f2: ', f1 ==f2) #f1 == f2:  False

#每次循环，都创建了一个新的函数，然后，把创建的3个函数都返回了
#返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9
def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i*i # 返回函数不要引用任何循环变量，或者后续会发生变化的变量
        fs.append(f) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs

f1, f2, f3 = count()
print('f1() = ', f1())     #9
print('f2() = ', f2())     #9
print('f3() = ', f3())     #9

#再创建一个函数，用该函数的参数绑定循环变量当前的值，无论该循环变量后续如何更改，已绑定到函数参数的值不变
def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1, 4):
        fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs

f1, f2, f3 = count()
print('f1() = ', f1())     #1
print('f2() = ', f2())     #4
print('f3() = ', f3())     #9




#============================
#匿名函数
#匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果
#
#lambda x: x * x (匿名函数)
#关键字lambda表示匿名函数，冒号前面的x表示函数参数
#等价于:
#def f(x):
#    return x * x
#============================
print('====lambda====')
print('lambda: ', list(map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9])))
#[1, 4, 9, 16, 25, 36, 49, 64, 81]

f = lambda x: x * x
print('f(5) = ', f(5))  # 5*5=25

#============================
#装饰器
#在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）
#函数对象有一个__name__属性
#============================

print('====装饰器:decorator====')
import functools

#两层嵌套的decorator
#def log(func):    #func = now
#    @functools.wraps(func)
#    return wrapper

#    def wrapper(*args, **kw):
#        print('call %s():' % func.__name__)
#        return func(*args, **kw)  #now()
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

@log   #等价于log(now)
def now():
    print('2015-3-25')

now()
#运行结果:
#call now():
#2015-3-25

#带参数的decorator
#def log(text):          #text = 'execute'      
#    return decorator
#
#    def decorator(func):  #func = now
#        return wrapper
#
#        def wrapper(*args, **kw):
#            print('%s %s():' % (text, func.__name__))
#            return func(*args, **kw)   #now()
def log2(text):                 
    def decorator(func): 
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log2('execute')
def now2():
    print('2015-3-25')

now2()
#运行结果:
#execute now2():
#2015-3-25

#============================
#偏函数
#functools.partial就是帮助我们创建一个偏函数
#functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单
#============================
print('====偏函数: functools.partial====')
import functools
print('int = ', int('1000000', base=2))  #64

int2 = functools.partial(int, base=2)    #64
print('int2 = ', int2('1000000'))
#============================
#============================
#============================
#============================

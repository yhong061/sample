#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#============================
#面向过程和面向对象的区别
#============================
#假设我们要处理学生的成绩表，为了表示一个学生的成绩
#
#1. 面向过程的程序可以用一个dict表示：
#   std1 = { 'name': 'Michael', 'score': 98 }
#   std2 = { 'name': 'Bob', 'score': 81 }
#而处理学生成绩可以通过函数实现，比如打印学生的成绩：
#  def print_score(std):
#      print('%s: %s' % (std['name'], std['score']))
#	
#2. 面向对象的程序设计思想，我们首选思考的不是程序的执行流程，而是Student这种数据类型应该被视为一个对象，
#这个对象拥有name和score这两个属性（Property）。
#如果要打印一个学生的成绩，首先必须创建出这个学生对应的对象，
#然后，给对象发一个print_score消息，让对象自己把自己的数据打印出来。
#
#  class Student(object):
#
#      def __init__(self, name, score):
#          self.name = name
#          self.score = score
#
#      def print_score(self):
#          print('%s: %s' % (self.name, self.score))
#		
#给对象发消息实际上就是调用对象对应的关联函数，我们称之为对象的方法（Method）。面向对象的程序写出来就像这样：
#  bart = Student('Bart Simpson', 59)
#  lisa = Student('Lisa Simpson', 87)
#  bart.print_score()
#  lisa.print_score()

#============================
# 类和实例
#
#定义类是通过class关键字
#class后面紧接着是类名，即Student，类名通常是大写开头的单词，紧接着是(object)，表示该类是从哪个类继承下来的
#定义好了Student类，就可以根据Student类创建出Student的实例，创建实例是通过类名+()实现的
#
#和普通的函数相比，在类中定义的函数只有一点不同，就是第一个参数永远是实例变量self，并且，调用时，不用传递该参数
#============================

#类
class Student(object):
    pass

#实例
bart = Student()

#__init__: 在创建实例的时候，把一些我们认为必须绑定的属性强制填写进去
#    __init__方法的第一个参数永远是self，表示创建的实例本身
#    创建实例的时候，传入与__init__方法匹配的参数，但self不需要传入
class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

bart = Student('Bart Simpson', 59)
print('bart.name = ', bart.name) #bart.name =  Bart Simpson


#数据封装: 类的方法
#        在Student类的内部定义访问数据的函数，这样，就把“数据”给封装起来了。
#        这些封装数据的函数是和Student类本身是关联起来的，我们称之为类的方法
class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score
		
    def print_score(self):   #类的方法
        print('%s: %s' % (self.name, self.score))

bart = Student('Bart Simpson', 59)
bart.print_score() #Bart Simpson: 59

#============================
#访问限制
#
#如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线__, 如__name, 为私有变量（private）
#不能直接访问__name是因为Python解释器对外把__name变量改成了_Student__name，所以，仍然可以通过_Student__name来访问__name变量
#变量名类似__xxx__的，也就是以双下划线开头，并且以双下划线结尾的，是特殊变量，特殊变量是可以直接访问的，不是private变量
#不同版本的Python解释器可能会把__name改成不同的变量名
#============================

#__name, __score
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))

#============================
#继承和多态
#
#继承
#当我们定义一个class的时候，可以从某个现有的class继承，新的class称为子类（Subclass），
#而被继承的class称为基类、父类或超类（Base class、Super class）
#
#多态
#当子类和父类都存在相同的run()方法时，子类的run()覆盖了父类的run()，
#在代码运行的时候，总是会调用子类的run()。
#============================

#继承
#----------------------------
#父类：
class Animal(object):
    def run(self):
        print('Animal is running...')

#子类：
class Dog(Animal):
    pass

#实例：
dog = Dog()
dog.run()
#Animal is running...

#多态
#----------------------------
class Dog(Animal):

    def run(self):
        print('Dog is running...')

#判断一个变量是否是某个类型可以用isinstance()判断
b = Animal() # b是Animal类型
c = Dog() # c是Dog类型
isinstance(b, Animal)
isinstance(c, Dog)

#多态的好处就是，当我们需要传入Dog、Cat、Tortoise……时，我们只需要接收Animal类型就可以了，
#因为Dog、Cat、Tortoise……都是Animal类型，然后，按照Animal类型进行操作即可。
#由于Animal类型有run()方法，因此，传入的任意类型，只要是Animal类或者子类，就会自动调用实际类型的run()方法，这就是多态的意思：
def run_twice(animal):
    animal.run()
    animal.run()

run_twice(Animal())
#Animal is running...
#Animal is running...
run_twice(Dog())
#Dog is running...
#Dog is running...

#============================
#静态语言 vs 动态语言
#============================
#对于静态语言（例如Java）来说，如果需要传入Animal类型，则传入的对象必须是Animal类型或者它的子类，否则，将无法调用run()方法。
#对于Python这样的动态语言来说，则不一定需要传入Animal类型。我们只需要保证传入的对象有一个run()方法就可以了

class Timer(object):
    def run(self):
        print('Start...')

#============================
#获取对象信息
#============================
#使用type()函数，来判断对象类型, 它返回对应的Class类型。
a = Animal() # b是Animal类型
print('type(a) = ', type(a))
#type(a) =  <class '__main__.Animal'>

#使用type()函数，来判断函数类型, 可以使用types模块中定义的常量。
import types
def fn():
    pass

type(fn)==types.FunctionType

#对于class的继承关系来说，使用type()就很不方便。
#我们要判断class的类型，可以使用isinstance()函数。
#能用type()判断的基本类型也可以用isinstance()判断
a = Animal()
d = Dog()

isinstance(d, Dog)
isinstance(d, Animal)

#如果要获得一个对象的所有属性和方法，可以使用dir()函数，它返回一个包含字符串的list
dir('ABC')

#getattr()、setattr()以及hasattr()
hasattr(a, 'x') # 有属性'x'吗？
setattr(a, 'y', 19) # 设置一个属性'y'
print('a.y = ', a.y)
#a.y =  19
getattr(a, 'y') # 获取属性'z'

#============================
#实例属性和类属性
#============================

#直接在class中定义属性，这种属性是类属性，归Student类所有
#这个属性虽然归类所有，但类的所有实例都可以访问到
class Student(object):
    name = 'Student'

s = Student() # 创建实例s
print(s.name) # 打印name属性，因为实例并没有name属性，所以会继续查找class的name属性
#Student
print(Student.name) # 打印类的name属性
#Student
s.name = 'Michael' # 给实例绑定name属性
print(s.name) # 由于实例属性优先级比类属性高，因此，它会屏蔽掉类的name属性
#Michael
print(Student.name) # 但是类属性并未消失，用Student.name仍然可以访问
#Student
del s.name # 如果删除实例的name属性
print(s.name) # 再次调用s.name，由于实例的name属性没有找到，类的name属性就显示出来了
#Student	

#============================
#给实例绑定属性和方法:
#============================

class Student(object):
    pass

#给实例绑定一个属性
s = Student()
s.name = 'Michael' # 动态给实例绑定一个属性 name
print(s.name)
#Michael

#给实例绑定一个方法
#但是，给一个实例绑定的方法，对另一个实例是不起作用的
def set_age(self, age): # 定义一个函数作为实例方法
    self.age = age

from types import MethodType
s.set_age = MethodType(set_age, s) # 给实例绑定一个方法
s.set_age(25) # 调用实例方法
print('s.age = ', s.age) # 测试结果
#s.age = 25

#为了给所有实例都绑定方法，可以给class绑定方法
def set_score(self, score):
    self.score = score

Student.set_score = set_score

#给class绑定方法后，所有实例均可调用
s.set_score(100)
print('s.score = ', s.score)
#100

#Python允许在定义class的时候，定义一个特殊的__slots__变量，来限制该class实例能添加的属性
#__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的
class Student(object):
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称

#============================
#属性的封装
#
#Python内置的@property装饰器就是负责把一个方法变成属性
#把一个getter方法变成属性，只需要加上@property就可以了，
#@property本身又创建了另一个装饰器@score.setter，负责把一个setter方法变成属性赋值，于是，我们就拥有一个可控的属性操作：
#============================

class Student(object):

    @property    #装饰器@property本身又创建了另一个装饰器@score.setter
    def score(self):             #score的get属性
        return self._score

    @score.setter
    def score(self, value):      #score的set属性
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

s = Student()
s.score = 60                 # OK，实际转化为s.set_score(60)
print('s.score = ', s.score) # OK，实际转化为s.get_score()
#s.score = 60

#只定义getter方法，不定义setter方法就是一个只读属性
#birth是可读写属性，而age就是一个只读属性，因为age可以根据birth和当前时间计算出来。

class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth

#============================
#多重继承

#假设我们要实现以下4种动物：
#Dog - 狗狗；
#Bat - 蝙蝠；
#Parrot - 鹦鹉；
#Ostrich - 鸵鸟。

#如果按照哺乳动物和鸟类归类，我们可以设计出这样的类的层次：
#哺乳类：能跑的哺乳类，能飞的哺乳类；
#鸟类：能跑的鸟类，能飞的鸟类
#============================

class Animal(object):
    pass

# 大类:
class Mammal(Animal):
    pass

class Bird(Animal):
    pass

class Runnable(object):
    def run(self):
        print('Running...')

class Flyable(object):
    def fly(self):
        print('Flying...')

# 各种动物:
class Dog(Mammal, Runnable):
    pass

class Bat(Mammal, Flyable):
    pass

class Parrot(Bird, Flyable):
    pass

class Ostrich(Bird, Runnable):
    pass

#============================
#定制类
#============================
#__str__: 针对于类， 返回用户看到的字符串
#__repr__: 针对于实例， 返回程序开发者看到的字符串

class Student(object):
    def __init__(self, name):
        self.name = name

print(Student('Michael'))
#<__main__.Student object at 0x109afb190>

class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Student object (name: %s)' % self.name

print(Student('Michael'))
#Student object (name: Michael)
s = Student('Michael')
print('s' = s)
#<__main__.Student object at 0x109afb310>

#__iter__
#如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法，
#该方法返回一个迭代对象，然后，Python的for循环就会不断调用该迭代对象的__next__()方法拿
#到循环的下一个值，直到遇到StopIteration错误时退出循环。

class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值

for n in Fib():
   print(n)

#__iter__()方法： 把对象视作list或tuple那样， 使用for ... in循环

#我们以斐波那契数列为例，写一个Fib类，可以作用于for循环：
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100000: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值

for n in Fib():
    print(n)

#__getitem__()方法，把对象视作list或dict来对集合获取值
#__setitem__()方法，把对象视作list或dict来对集合赋值。
#__delitem__()方法，用于删除某个元素。

#Fib实例虽然能作用于for循环，看起来和list有点像，但是，把它当成list来使用还是不行，比如，取第5个元素
#Fib()[5]  #Traceback
#要表现得像list那样按照下标取出元素，需要实现__getitem__()方法：
class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a

f = Fib()
f[0]
f[1]
#============================
#============================

#============================
#============================

#============================
#============================

#============================
#============================





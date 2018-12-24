#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#============================
#datetime是Python处理日期和时间的标准库。
#============================

#获取当前日期和时间: datetime.now()
from datetime import datetime  #如果仅导入import datetime，则必须引用全名datetime.datetime。
now = datetime.now() # 获取当前datetime
print(now)
print(type(now))  #<class 'datetime.datetime'>

#获取指定日期和时间: datetime(data & time)
dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
print(dt)


#datetime转换为timestamp: timestamp()
dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
dt.timestamp() # 把datetime转换为timestamp
#1429417200.0  #Python的timestamp是一个浮点数。如果有小数位，小数位表示毫秒数。

#timestamp转换为datetime: fromtimestamp()
t = 1429417200.0
print(datetime.fromtimestamp(t)) # 本地时间
print(datetime.utcfromtimestamp(t)) # UTC时间

#str转换为datetime
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')

#datetime转换为str
now = datetime.now()
print(now.strftime('%a, %b %d %H:%M'))

#datetime加减
from datetime import datetime, timedelta
now = datetime.now()
now + timedelta(hours=10)
now - timedelta(days=1)
now + timedelta(days=2, hours=12)

#本地时间转换为UTC时间
from datetime import datetime, timedelta, timezone
tz_utc_8 = timezone(timedelta(hours=8)) # 创建时区UTC+8:00
now = datetime.now()
dt = now.replace(tzinfo=tz_utc_8) # 强制设置为UTC+8:00

#时区转换
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc) #拿到当前的UTC时间
# astimezone()将转换时区为北京时间:
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
# astimezone()将转换时区为东京时间:
tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
# astimezone()将bj_dt转换时区为东京时间:
tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9)))

#============================
#============================
#============================
#============================
#============================
#============================
#============================
#============================



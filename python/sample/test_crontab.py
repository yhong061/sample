# sudo python3 -m pip uninstall crontab
# sudo python3 -m pip install python-crontab
# sudo python3 -m pip install croniter

#class CronTab(builtins.object)
#   ----Crontab object which can access any time based cron using the standard.----
#*   CronTab(user=None, tab=None, tabfile=None, log=None)
#   append(self, item, line='', read=False)
#   find_command(self, command)
#   find_comment(self, comment)
#   find_time(self, *args)
#*   new(self, command='', comment='', user=None)   #Returns the new CronItem object
#   read(self, filename=None)
#   remove(self, *items)
#*   remove_all(self, *args, **kwargs)
#   render(self, errors=False)
#   run_pending(self, **kwargs)
#   run_scheduler(self, timeout=-1, **kwargs)
#*   write(self, filename=None, user=None, errors=False)
#   write_to_user(self, user=True)

#class CronItem(builtins.object)
#   ----An item which objectifies a single line of a crontab and May be considered to be a cron job object. ----
#   CronItem(command='', comment='', user=None, cron=None)
#   clear(self)
#   delete(self)
#   description(self, **kw)
#   enable(self, enabled=True)
#   every(self, unit=1)
#   every_reboot(self)
#   frequency(self, year=None)
#   frequency_per_day(self)
#   frequency_per_hour(self)
#   frequency_per_year(self, year=None)
#   is_enabled(self)
#   is_valid(self)
#   parse(self, line)
#   render(self)
#   run(self)
#   run_pending(self, now=None)
#   schedule(self, date_from=None)
#   set_command(self, cmd)
#   set_comment(self, cmt)
#   setall(self, *args)

import datetime
from crontab import CronTab

cron = CronTab(user='yhong')
cron.remove_all()


#Create job with comment
job = cron.new(command='/usr/local/bin/python3.7 EDA-Robot/EDA-Robot.py', comment='EDA-Robot')  

print ("Set job running time")
#job.minute.during(5,50).every(5)
#job.hour.every(4)
#job.day.on(4, 5, 6)
#job.dow.on('SUN', 'FRI')
#job.month.during('APR', 'NOV')
job.minute.every(3)

#job_standard_output = job.run()          #run job now
#print ("print job comment", job.comment) 
#print ("print job command", job.command)
#job.set_command("new_command.sh")        #set job command
#job.set_comment("new comment ID")        #set job comment
#job.enable()
#job.enable(False)                        #disable job
#False == job.is_enbale()
#True == job.is_valid()
#job.clear                                #clear job all rules


cron.write()
print ("EDA-Robot job created")

print ("list current cron job according comment")
joblist = cron.find_comment('EDA-Robot')
for item in joblist:  
    print (item)

print ("list current cron job according command")
joblist = cron.find_command('/usr/local/bin/python3.7 EDA-Robot/EDA-Robot.py')
for item in joblist:  
    print (item)

for job1 in cron:
    print (job)
    sch = job1.schedule(date_from=datetime.datetime.now())
    print (sch.get_next())

for line in cron.lines:
    print (line)


cron.remove_all(command='/usr/local/bin/python3.7 DA-Robot/EDA-Robot.py')
cron.remove_all(comment='EDA-Robot')
cron.remove_all(time='* * * * *')
cron.remove_all()


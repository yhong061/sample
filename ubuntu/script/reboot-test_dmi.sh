#!/bin/bash
# reboot test
#set -x
KMSG=/dev/kmsg
LOG=/root/reboot.log
script=$0
stop_on_error=0

# get current date;
date=$(date -Iseconds)

ncpu=$(grep -c processor /proc/cpuinfo)
case $ncpu in
4)
	sys=edge3200
	;;
8)
	sys=edge3400
	;;
16)
	sys=edge3800
	;;
*)
	echo "error: unexpected # of cores"
	exit 1
esac

check_BIOS() {
	ret=$(/usr/bin/ipmitool raw 0x3a 0x06 0x00)
	if [ $ret == 00 ];then
	    echo "===========Primary BIOS============"  >> $LOG
	else
	    echo "===========Backup BIOS============="   >> $LOG
	    exit
	fi
}

rm_var_log() {
	rm /var/log/auth.log
	rm /var/log/daemon.log
	rm /var/log/debug
	rm /var/log/kern.log
	rm /var/log/messages
	rm /var/log/syslog
}

update_log() {
	echo -e "\n$date reboot test run on $sys" >> $LOG
	echo "# $date reboot test run" > $KMSG
	# get current date;
	date=$(date -Iseconds)
	# execute command to cause reboot;
	date=$(date -Iseconds)
	echo "$date issue '$cmd'" >> $LOG
	echo "# $date issue '$cmd'" > $KMSG
	sync
	sync
}

reboot_sys() {
      # create random wait;
      # also, give us 10 secs to kill this program;
      date=$(date -Iseconds)
      rand=$RANDOM
      wait=$(((($rand >> 4) & 0x3f) + 10))

      # log next expected type;
      echo "$date wait ${wait}s next '$msg' pst=$type" >> $LOG
      echo "# $date wait ${wait}s next '$msg' pst=$type" > $KMSG
      sleep $wait

      # report if are still alive;
      delay=20
      sleep $delay
      date=$(date -Iseconds)
      echo "$date +${delay}s unexpectedly still alive" >> $LOG
      echo "# $date +${delay}s unexpectedly still alive" > $KMSG
      #reboot
      rm_var_log
      /usr/bin/ipmitool chassis power reset
      sync
      sync
      sleep 1
}

run_dmi_test() {
	files=(
	       "dmidecode -t 0 | grep -v point" 
	       "dmidecode -t 1 | grep -v point" 
	       "dmidecode -t 2 | grep -v point" 
	)

	dmi_error=0
	update_log
	for cmd in "${files[@]}" ; do 
	      current_log="/root/log_current_${cmd}"
	      current_log=$(tr -d ' ' <<< "$current_log")
	      prev_log="/root/log_prev_${cmd}"
	      prev_log=$(tr -d ' ' <<< "$prev_log")
	      first_log="/root/log_first_${cmd}"
	      first_log=$(tr -d ' ' <<< "$first_log")
	      eval $cmd > "$current_log"
              if [ -f $prev_log ]; then
		 diffs=$(diff $current_log $prev_log)
		 if [ $? -ne 0 ]; then
		   dmi_error=1
		   echo "error : DMI info corrupted  $cmd output is not same" >> $LOG
		   echo "====current output====" >> $LOG
		   cat $current_log >> $LOG
		   echo "====previous output====" >> $LOG
		   cat $prev_log >> $LOG
	        fi
	     else
	        cp $current_log $first_log
	     fi
	     mv $current_log $prev_log
	done
	if [ $dmi_error != "1" ]; then
	     echo "success : DMI info is  same" >> $LOG
	     echo "success : DMI info is  same" >> $KMSG
	else
	   echo "dmierr : DMI information changed, output is not same" >> $LOG
	   echo "dmierr : DMI information changed, output is not same" >> $KMSG
	   if [ $stop_on_error == 1 ]; then
		echo "====stopping test====" >> $LOG
		echo "====stopping test====" >> $KMSG
	        exit
	   fi
	fi
	reboot_sys
}

# handle commands;
case $1 in
help)
	echo " help            - this"
	echo " run             - run the reboot-test"
	echo " analyze         - analyze the log for errors"
	exit 0
	;;
run)
	if [ ! -z $2 ] && [ $2 == "stop" ]; then
	    stop_on_error=1
	    echo "$stop_on_error"
	fi
        check_BIOS
	run_dmi_test
	;;
# stop the test;
stop)
	echo "$date test stopped" >> $LOG
	killall $script
	#mv $0 /root/script_2
	cp /etc/rc.local_org /etc/rc.local
	exit 0
	;;
# analyze log;
analyze)
	if [ -n "$2" ]; then
		LOG=$2
	fi
	nrun=$(grep 'reboot test run' $LOG | wc -l)
	nerr=$(grep dmierr $LOG | wc -l)
	echo "$nrun runs, $nerr errors"
	grep error $LOG | cut -f3- -d' ' | sort | uniq -c
	nsuc=$(grep success $LOG | wc -l)
	echo "$nrun runs, $nsuc success"
	grep success $LOG | cut -f3- -d' ' | sort | uniq -c
	exit 0
	;;
*)
	echo "# error: unknown command $1" > $KMSG
	exit 1
esac
exit 0

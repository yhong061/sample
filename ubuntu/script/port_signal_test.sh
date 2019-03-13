#!/bin/bash

busnum=$(pcitool --scan | grep Xilinx | sed 's/:/ /g' | sed 's/\./ /g' | awk '{print $5}')
devnum=$(pcitool --scan | grep Xilinx | sed 's/:/ /g' | sed 's/\./ /g' | awk '{print $6}')
funid=$(pcitool --scan | grep Xilinx | sed 's/:/ /g' | sed 's/\./ /g' | awk '{print $7}')
#echo "$busnum	 $devnum  $funid" 

byte4=$(pcitool --read --bus=$busnum --dev=$devnum --func=$funid --offset=0x10 --count=4 | sed 's/0x/ /g' | awk '{print $5}')  
byte3=$(pcitool --read --bus=$busnum --dev=$devnum --func=$funid --offset=0x10 --count=4 | sed 's/0x/ /g' | awk '{print $4}')  
byte2=$(pcitool --read --bus=$busnum --dev=$devnum --func=$funid --offset=0x10 --count=4 | sed 's/0x/ /g' | awk '{print $3}')	
byte1=$(pcitool --read --bus=$busnum --dev=$devnum --func=$funid --offset=0x10 --count=4 | sed 's/0x/ /g' | awk '{print $2}')
#echo "address: 0x$byte4$byte3$byte2$byte1" 
FPGA_BASE_ADDR=0x$byte4$byte3$byte2$byte1

BRD_TYPE_Z9232_NON_NEBS=0x0
BRD_TYPE_Z9232_NEBS=0x1
BRD_TYPE_Z9264_NON_NEBS=0x2
BRD_TYPE_Z9264_NEBS=0x3
BRD_TYPE_S5212_NON_NEBS=0x4
BRD_TYPE_S5212_NEBS=0x5
BRD_TYPE_S5224_NON_NEBS=0x6
BRD_TYPE_S5224_NEBS=0x7
BRD_TYPE_S5248_NON_NEBS=0x8
BRD_TYPE_S5248_NEBS=0x9
BRD_TYPE_S5296_NON_NEBS=0xa
BRD_TYPE_S5296_NEBS=0xb
BRD_TYPE_S5232_NON_NEBS=0xc
BRD_TYPE_S5232_NEBS=0xd

PORT_BASE=0x4000
PRSNT_MASK=4
TXFAULT_MASK=2
RXLOS_MASK=1
MODABS_MASK=0

get_bits(){
	local data=$1
	local offset=$2
	local bits=$3
	local tmp

	tmp=$(((((1<<$bits)-1)<<$offset)&$data))
    echo $(($tmp>>$offset))
}

get_mem_byte() {
	local reg=$1
	echo $(memtool -r -a $reg -C 1 -W 8  | grep "||"  | awk '{ print $2}')
}

set_mem_byte() {
	local reg=$1
	local data=$2
	$(memtool -w -a $reg -V $data -C 1 -W 8)
}

get_i2c_byte() {
	local bus=$1
	local addr=$2
	local reg=$3
	echo $(i2cget -y $bus $addr $reg)
}

set_i2c_byte() {
	local bus=$1
	local addr=$2
	local reg=$3
	local data=$4
	$(i2cset -y $bus $addr $reg $data)
}

board_detect(){
    local ret_val
	local register_offset

	register_offset=$(($FPGA_BASE_ADDR+0x8))
	register_offset=$(printf "0x%X" $register_offset)	
    ret_val=$(get_mem_byte $register_offset)
    #echo $register_offset " = " $ret_val

    ret_val=$(get_bits $ret_val 0 4) 
    #echo "get board" $ret_val $(($BRD_TYPE_S5296_NON_NEBS)) 

	if [ $ret_val -eq $(($BRD_TYPE_S5212_NON_NEBS)) -o $ret_val -eq $(($BRD_TYPE_S5212_NEBS)) ];then
		echo "board_S5212"
	elif [ $ret_val -eq $(($BRD_TYPE_S5224_NON_NEBS)) -o $ret_val -eq $(($BRD_TYPE_S5224_NEBS)) ];then
		echo "board_S5224"    
	elif [ $ret_val -eq $(($BRD_TYPE_S5232_NON_NEBS)) -o $ret_val -eq $(($BRD_TYPE_S5232_NEBS)) ];then
		echo "board_S5232"
	elif [ $ret_val -eq $(($BRD_TYPE_S5248_NON_NEBS)) -o $ret_val -eq $(($BRD_TYPE_S5248_NEBS)) ];then
        echo "board_S5248"
    elif [ $ret_val -eq $(($BRD_TYPE_S5296_NON_NEBS)) -o $ret_val -eq $(($BRD_TYPE_S5296_NEBS)) ];then
        echo "board_S5296"
	else
		echo "board_unkonw"
	fi

}

detect_SFP_signal(){
   local ret_val
   local register_offset
   local signal
   local port_addr=$FPGA_BASE_ADDR+$PORT_BASE
   local status_offset=0x4
   local idx=$1
   
   printf "%10s%8s|" SFP-$idx
   register_offset=$(($port_addr+$status_offset+($idx-1)*16))
   register_offset=$(printf "0x%X" $register_offset)   
   ret_val=$(get_mem_byte $register_offset)
   #echo $register_offset " " $ret_val
   
   signal=$(get_bits $ret_val $MODABS_MASK 1)
   if [ $signal -eq 0 ];then
       printf "%15s%-8s|" Present 
   elif [ $signal -eq 1 ];then
       printf "%15s%-8s|" "No Present"  
   else
      printf "%15s %-8s|" "Unknown signal"
   fi
 
   signal=$(get_bits $ret_val $TXFAULT_MASK 1)
   if [ $signal -eq 0 ];then
       printf "%15s%-8s|" "No TX Fault"
   elif [ $signal -eq 1 ];then
       printf "%15s%-8s|" "TX Fault"
   else
      printf "%15s%-8s|" "Unknown signal"
   fi
   
   signal=$(get_bits $ret_val $RXLOS_MASK 1)
   if [ $signal -eq 0 ];then
       printf "%15s%-8s|\n" "No RX Loss"
   elif [ $signal -eq 1 ];then
       printf "%15s%-8s|\n" "RX Loss"
   else
      printf "%15s%-8s|\n" "Unknown signal"
   fi
   
}  

detect_QSFP_signal(){
   local ret_val
   local register_offset
   local signal
   local port_addr=$FPGA_BASE_ADDR+$PORT_BASE
   local status_offset=0x4
   local idx=$1
   
   printf "%10s%8s|" QSFP-$idx
   register_offset=$(($port_addr+$status_offset+($idx-1)*16))
   register_offset=$(printf "0x%X" $register_offset)   
   ret_val=$(get_mem_byte $register_offset)
   #echo $register_offset " " $ret_val

   signal=$(get_bits $ret_val $PRSNT_MASK 1)
   if [ $signal -eq 0 ];then
      printf "%15s%-8s|\n" Present
   elif [ $signal -eq 1 ];then
      printf "%15s%-8s|\n" "No Present"
   else
      printf "%15s%-8s|\n" "Unknown signal"
   fi
   
}

detect_all_SFP_signal() {
	local start=$1
	local end=$2
    for ((i=$start; i<=$end; i++))
    do
        detect_SFP_signal $i
    done
}

detect_all_QSFP_signal() {
	local start=$1
	local end=$2
	for ((i=$start; i<=$end; i++))
	do
		detect_QSFP_signal $i
	done
}

#QSFP DD test steps:
#MODSEL/LPMOD
#0x8b[1] InitMode  Digital state of InitMode
#root@dellemc-diag-os:~# memtool --write --addr=0xdfc04300 --val=0x51           //set MODESEL=0,RST=1
#root@dellemc-diag-os:~# i2cset -y 20 0x74 0x0 0x01
#root@dellemc-diag-os:~# i2cset -y 20 0x50 0x7f 0x2
#root@dellemc-diag-os:~# i2cget -y 20 0x50 0x8b                                 //MODSEL=0,LPMOD=1
#0x22
#root@dellemc-diag-os:~# memtool --write --addr=0xdfc04300 --val=0x11           //set LPMOD
#root@dellemc-diag-os:~# i2cget -y 20 0x50 0x8b                                 //MODSEL=0,LPMOD=0
#0x20

detect_QSFP_DD_signal(){
   local ret_val
   local signal
   local test_flag=0
   local register_offset
   local port_addr=$FPGA_BASE_ADDR+$PORT_BASE
   local control_offset=0x0
   local i2c_mux_addr=0x74
   local i2c_qsfpDD_addr=0x50
   local idx=$1
   local bus=$2
   local mux=$3

   register_offset=$(($port_addr+$control_offset+($idx-1)*16))
   register_offset=$(printf "0x%X" $register_offset)

   set_mem_byte $register_offset 0x71
   sleep 0.03

   set_mem_byte $register_offset 0x51
   sleep 0.03

   set_i2c_byte $bus $i2c_mux_addr 0x00 $mux
   sleep 0.03

   set_i2c_byte $bus $i2c_qsfpDD_addr 0x7f 0x2
   sleep 0.03

   ret_val=$(get_i2c_byte $bus $i2c_qsfpDD_addr 0x8b)
   #echo "0. 0x8b=" $ret_val

   signal=$(get_bits $ret_val 1 1)
   if [ $signal -eq 1 ];then
       test_flag=$(($test_flag+1))
   else
       test_flag=$(($test_flag*0))
   fi
   
   set_mem_byte $register_offset 0x11
   sleep 0.03
   
   ret_val=$(get_i2c_byte $bus $i2c_qsfpDD_addr 0x8b)
   #echo "1. 0x8b=" $ret_val

   signal=$(get_bits $ret_val 1 1)
   if [ $signal -eq 0 ];then
       test_flag=$(($test_flag+1))
   else
       test_flag=$(($test_flag*0))
   fi

   set_mem_byte $register_offset 0x71
   
   if [ ! $test_flag -eq 0 ];then   	
	   printf "%10s%8s|        test ................... [ Passed ]\n" QSFP-DD-$idx
   else
	   printf "%10s%8s|        test ................... [ Failed ]\n" QSFP-DD-$idx
   fi   
}

detect_all_ports(){
   local board_type
   local start 
   local end
   	
   board_type=$(board_detect)
   printf "\n%25s############### $board_type ###############\n\n" 

   if [ $board_type == "board_S5212" ];then
   	   start=1
   	   end=12
       detect_all_SFP_signal $start $end
       
	   start=13
	   end=15
       detect_all_QSFP_signal $start $end
       
   elif [ $board_type == "board_S5224" ];then
   	   start=1
   	   end=24
       detect_all_SFP_signal $start $end
       
	   start=25
	   end=28
       detect_all_QSFP_signal $start $end
       
   elif [ $board_type == "board_S5232" ];then
   	   start=1
   	   end=32
       detect_all_QSFP_signal $start $end
       
	   start=33
	   end=34
       detect_all_SFP_signal $start $end

   elif [ $board_type == "board_S5248" ];then
   	   local bus=20

   	   start=1
   	   end=48
       detect_all_SFP_signal $start $end
  
       detect_QSFP_DD_signal 49 $bus 1
       detect_QSFP_DD_signal 51 $bus 2
       
	   start=53
	   end=56
       detect_all_QSFP_signal $start $end

   elif [ $board_type == "board_S5296" ];then
   	   start=1
   	   end=96
       detect_all_SFP_signal $start $end
       
	   start=97
	   end=102
       detect_all_QSFP_signal $start $end

   else
       echo "Unknown board"
       exit 1
   fi
 
}

detect_all_ports

#!/bin/bash

i2ctool="ipmitool raw 0x3a 0x01 "
dev_bus=0x06
dev_addr=0xb0

pmbus_linear_convert(){
	input=$1
	N=1
	i=0
	
	let 'v = input & 0x0400'

	if [ $v -eq 0 ]; then
		let 'a = input & 0x03FF'
	else	
		let 'a = input | 0xF800'
	fi	
	
	let 'v = input & 0x8000'
	
	if [ $v -eq 0 ]; then
		let 'n = ((input & 0x7800) >> 11) & 0x0F'
		while [ "$i" -lt "$n" ]; do
			let 'N = 2 * N'
			let 'i += 1'
		done	
		let 'ret = a * N'
	else
		let 'n = ((~((input & 0x7800) >> 11)) + 1) & 0x0F'
		while [ "$i" -lt "$n" ]; do
			let 'N = 2 * N'
			let 'i += 1'
		done	
		let 'ret = a / N'
	fi
	
	echo $ret
}

pmbus_cmd_read(){
	local bus=$1
	local addr=$2
	local reg=$3
	echo $(${i2ctool} ${bus} ${addr} 0x02 ${reg})
}

pmbus_cmd_write(){
	local bus=$1
	local addr=$2
	local reg=$3
	let 'val_h = (($4 & 0xFF00) >> 8) & 0xFF'
	let 'val_l = ($4 & 0x00FF)'
	echo "val_h:" ${val_h}
	echo "val_l:" ${val_l}
	${i2ctool} ${bus} ${addr} 0x00 ${reg} ${val_h} ${val_l}
}

pmbus_read() {
	ret=$(pmbus_cmd_read $1 $2 $3)
	echo $ret>/tmp/diag.log
}

pmbus_fan_write() {
	local reg=0x3b
	pmbus_cmd_write $1 $2 ${reg} $3
}

fan_read() {
	pmbus_read $1 $2 $3

	eval $(awk '{if ($2 ~ /^[0-9a-f][0-9a-f]/) printf("high=%s;low=%s",$2,$1)}' /tmp/diag.log)
	let high="0x"$high 
	let low="0x"$low 
	let 'val=(high << 8)+low'
	echo $val
}

pmbus_info() {
	local reg
	local ret
	
	echo -n PSU FAN Speed: 
	reg=0x90
	ret=$(fan_read $1 $2 ${reg})
	pmbus_linear_convert $ret

}

pmbus_info ${dev_bus} ${dev_addr}



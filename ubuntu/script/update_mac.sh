#!/bin/bash

PATTERN='^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
net_rules_file="/etc/udev/rules.d/70-persistent-net.rules"

print_usage() {
    echo "Need NIC name"
    echo "usage: $0 eth0 00:11:22:33:44:55"
}

if [ -z $1 ]; then
    print_usage $0
    exit 1
else
    dev=$1
fi

if [ -z $2 ]; then
    print_usage $0
    exit 1
else
    mac=$2
fi

# Check MAC address
ethtool $dev > /dev/null
if [[ $? -ne 0 ]]; then
    echo "Invalid NIC name $dev"
    print_usage $0
    exit 1
fi

# Check MAC address
if [[ ! "$mac" =~ $PATTERN ]]; then
    echo "Invalid mac address"
    print_usage $0
    exit 1
fi

if [ "$1" == "eth0" ] ; then
    base_addr=0x288
elif [ "$1" == "eth1" ]; then
    base_addr=0x28e
elif [ "$1" == "eth2" ]; then
    base_addr=0x288
elif [ "$1" == "eth3" ]; then
    base_addr=0x28e
fi

pci_bus=`ethtool -i $1 | grep bus-info | sed -e 's/bus-info: //'`

magic_number=$(lspci -s $pci_bus -x | head -n 2 | tail -n 1 | awk '{print $5$4$3$2}')

# Update MAC address
for ((i=0; i<6; i++))
do
    tmp=`expr $i + 1`
    val=`echo $mac | awk -F ':' -v "v=$tmp" '{print $v}'`

    ethtool -E $dev magic 0x$magic_number offset $(($i + $base_addr)) value 0x$val
done

if [ -e $net_rules_file ]; then
    rm $net_rules_file
fi

sync
echo "Update MAC address complete."

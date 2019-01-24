#!/bin/bash

TOOL=ledtool

set()
{
    echo ${TOOL}" --set --led="$1" --$3="$2
    ${TOOL} --set --led=$1 --$3=$2
}

get()
{
    echo  ${TOOL}" --get --led="$1
    ${TOOL} --get --led=$1
}

set_val()
{
    set $1 $2 val
    get $1
}

set_vals()
{
    get $1
    printf "\n"

    #parse input params from $2, $3, ...
    for i in "${@:2}"
    do
        set_val $1 ${i}
        printf "\n"
    done
}

set_state()
{
    set $1 $2 state
    get $1
}

set_states()
{
    get $1
    printf "\n"

    #parse input params from $2, $3, ...
    for i in "${@:2}"
    do
        set_state $1 ${i}
        printf "\n"
    done
}

set_states 7-digit off blink-green solid-green
set_vals Stack-val 0x39 0x38

#test result:  
#
#root@dellemc-diag-os:/home/yana24x# ./led3.sh
#ledtool --get --led=7-digit
#7-digitled: solid-green
#
#ledtool --set --led=7-digit --state=off
#ledtool --get --led=7-digit
#7-digitled: off
#
#ledtool --set --led=7-digit --state=blink-green
#ledtool --get --led=7-digit
#7-digitled: blink-green
#
#ledtool --set --led=7-digit --state=solid-green
#ledtool --get --led=7-digit
#7-digitled: solid-green
#
#ledtool --get --led=Stack-val
#Stack-valled: Value 0x38
#
#ledtool --set --led=Stack-val --val=0x39
#ledtool --get --led=Stack-val
#Stack-valled: Value 0x39
#
#ledtool --set --led=Stack-val --val=0x38
#ledtool --get --led=Stack-val
#Stack-valled: Value 0x38




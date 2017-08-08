#!/bin/bash

CID_array=( $(docker ps --no-trunc -q --filter ancestor=sai6kiran/waggle-vne-image:2.6.0-pre1|head) )
for i in "${CID_array[@]}"
do
    if [[ -z $i ]]; then
	echo 'CID not found'
	exit
    fi
    
    USBDEV=( $(readlink -f /dev/waggle_coresense[0-9]*) )
    for j in "${USBDEV[@]}"
    do
	read minor major < <(stat -c '%T %t' $j)
	if [[ -z $minor || -z $major ]]; then
	    echo 'Device not found'
	    exit
	fi
	dminor=$((0x${minor}))
	dmajor=$((0x${major}))
    
	echo 'Setting permissions'
	echo "c $dmajor:$dminor rwm" > /sys/fs/cgroup/devices/docker/$i/devices.allow
    done
done


#!/bin/bash
set -x

read -p 'Are you sure add `nbs` into all flavor now?[y/n]' ans
if [ "${ans}s" != "ys" ] 
then
    exit 1
fi

for i in `nova-manage flavor list |awk -F: '{print $1}'`
do 
    nova-manage flavor set_key --name $i  --key nbs --value true
done

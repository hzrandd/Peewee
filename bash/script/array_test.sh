#!/bin/bash
for ((i=0; i<10; i++))
do
    array[$i]=$i
done
for ((i=0; i<10; i++))
do
    echo ${array[$i]}
done

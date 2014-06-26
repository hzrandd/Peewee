#!/bin/bash
#This file is used to explain the shell system variable.
#set -x
echo "the number of parameter is $# ";
echo "the return code of last command is $?";
echo "the script name is $0 ";
echo "the parameters are $* ";
echo "the parameters are $@ ";
echo "$1 = $1 ; \$2 = $2 ";
re=$*
qw=$@
echo "\$re = $re"
echo "\$qw = $qw"
##############################################
name[0]="Tom"
name[1]="Tomy"
name[2]="John"
echo "\$name[0] = ${name[0]}"
echo "\$name[1] = ${name[1]}"
###############################################
name=("Tom" "Tomy" "John", "hello")
for i in 0 1 2 3 4 5
do
    echo $i:${name[$i]} ;
done;

#set +x
#####################################################
if [ $# -ne 2 ] ; then
   echo "Usage: $0 string file";
  exit 1;
 fi
grep $1 $2 ;
if [ $? -ne 0 ] ; then
   echo "Not Found \"$1\" in $2";
  exit 1;
 fi
echo "Found \"$1\" in $2"; 
#####################################################

echo 'ip'
echo 'ip=$ip'
echo `$($ip)`
echo $($ip)
echo ip


#!/bin/bash

# usage: 
# ./cgexec.sh cpu:g1,memory:g2/g21 sleep 100

blkio_dir="/sys/fs/cgroup/blkio"
memory_dir="/sys/fs/cgroup/memory"
cpuset_dir="/sys/fs/cgroup/cpuset"
perf_event_dir="/sys/fs/cgroup/perf_event"
freezer_dir="/sys/fs/cgroup/freezer"
net_cls_dir="/sys/fs/cgroup/net_cls"
cpuacct_dir="/sys/fs/cgroup/cpuacct"
cpu_dir="/sys/fs/cgroup/cpu"
hugetlb_dir="/sys/fs/cgroup/hugetlb"
devices_dir="/sys/fs/cgroup/devices"

groups="$1"
shift

IFS=',' g_arr=($groups)
for g in ${g_arr[@]}; do
  IFS=':' g_info=($g)
  if [ ${#g_info[@]} -ne 2 ]; then
    echo "bad arg $g" >&2
    continue
  fi
  g_name=${g_info[0]}
  g_path=${g_info[1]}
  if [ "$g_path" == "${g_path#/}" ]; then
    g_path="/$g_path"
  fi
  echo $g_name $g_path
  var="${g_name}_dir"
  d=${!var}
  if [ -z "$d" ]; then
    echo "bad cg name $g_name" >&2
    continue
  fi
  path="${d}${g_path}"
  if [ ! -d "$path" ]; then
    echo "cg not exists" >&2
    continue
  fi
  echo "$$" >"${path}/tasks"
done

exec $*


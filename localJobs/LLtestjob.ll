#@ shell = /bin/bash
#@ job_name         = getting_started_job
#@ class            = default
#@ group            = nesi
#@ account_no       = uoa99999
#@ wall_clock_limit = 00:01:00
#@ resources        = ConsumableMemory(8096mb) ConsumableVirtualMemory(8096mb)
#@ initialdir = /projects/uoa99999/ccah002/9apr/LLtest/localJobs
#@ job_type         = serial
#@ output = ../actualOutput/javajob.txt
#@ error = ../errors/javajob.txt
#@ notification     = never
#@ queue

let "limit = 8096 * 1024"
ulimit -v ${limit} -m ${limit}

#java javaJob.jar
/share/apps/smpexec  -s  java  '-XX:MaxHeapSize=64m' '-Xmx128m' 'testJobMain'




#@ shell = /bin/bash
#@ job_name         = getting_started_job
#@ class            = default
#@ group            = nesi
#@ account_no       = uoa99999
#@ wall_clock_limit = 00:01:00
#@ resources        = ConsumableMemory(2048mb) ConsumableVirtualMemory(2048mb)
#@ initialdir = /projects/uoa99999/ccah002/9apr/LLtest/localJobs
#@ job_type         = parallel
#@ total_tasks = 4
#@ blocking = unlimited
#@ output = ../actualOutput/rMPIjob.txt
#@ error = ../errors/rMPIjob.txt
#@ notification     = never
#@ queue

let "limit = 2048 * 1024"
ulimit -v ${limit} -m ${limit}

mpirun --hostfile $LOADL_HOSTFILE RMPISNOW -f generateIntermediates.r --args 4 20000

cat finalresult.txt
rm inter*
rm finalresult.txt


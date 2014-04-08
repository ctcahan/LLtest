#@ shell = /bin/bash
#@ job_name         = getting_started_job
#@ class            = default
#@ group            = nesi
#@ account_no       = uoa99999
#@ wall_clock_limit = 00:01:00
#@ resources        = ConsumableMemory(2048mb) ConsumableVirtualMemory(2048mb)
#@ initialdir = /projects/uoa99999/ccah002/9apr/LLtest/localJobs
#@ job_type         = serial
#@ output = ../actualOutput/rjob1.txt
#@ error = ../errors/rjob1.txt
#@ notification     = never
#@ queue

let "limit = 2048 * 1024"
ulimit -v ${limit} -m ${limit}

R -f /projects/uoa99999/ccah002/testSuite/testCases/rtest.R



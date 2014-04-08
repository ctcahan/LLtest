#!/usr/bin/python

# script to help create a new test case for a program
# arguments:
	#(programName[, jobName, jobLLPath, jobTestScriptPath, fileOne, fileOneName])

import os, sys, subprocess

nargs = len(sys.argv)-1
programName = sys.argv[1]
jobName = sys.argv[2]




p = subprocess.Popen("pwd", stdout = subprocess.PIPE, shell=True)
(currDir, err)  = p.communicate()
currDir = currDir.strip()
#os.system("mkdir -p " + programName)

miscProgs = os.path.join(currDir, "miscProgs")

if not os.path.isdir(miscProgs):
	os.system("mkdir miscProgs")

os.system("mkdir -p miscProgs/" + programName)
os.system("mkdir -p miscProgs/" + programName + "/jobs")
os.system("mkdir -p miscProgs/" + programName + "/jobs/" + jobName)
os.system("mkdir -p miscProgs/" + programName + "/jobs/" + jobName + "/files")
os.system("mkdir -p miscProgs/" + programName + "/tests/")
os.system("mkdir -p miscProgs/" + programName + "/tests/" + jobName)
os.system("mkdir -p miscProgs/" + programName + "/tests/" + jobName + "/scripts")


if nargs > 2:
	jobLLPath = sys.argv[3]
	os.system("cp " + jobLLPath + " miscProgs/" + programName + "/jobs/" + jobName + "/job.ll")

if nargs > 3:
	jobTestScriptPath = sys.argv[4]
	os.system("cp " + jobTestScriptPath + " miscProgs/" + programName + "/tests/" + jobName + "/scripts/scriptLL.py")
	os.system("chmod a+x " + "miscProgs/" + programName + "/tests/" + jobName + "/scripts/scriptLL.py")

if nargs > 4:
	fileOne = sys.argv[5]
	fileOneName = sys.argv[6]
	os.system("cp " + jobLLPath + " miscProgs/" + programName + "/jobs/files/" + fileOneName)





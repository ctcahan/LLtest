#!/usr/bin/python


# USAGE:	for programA, jobNameB
#	create .ll job submission file in directory /applications/programA/jobs/jobNameB/__.ll
#	create matching test script in directory /application/programA/tests/jobNameB/scripts/__.py
#
# EXAMPLE test script: 
#### #!/usr/bin/python
#### import os, sys, subprocess
#### 
#### filePath = sys.argv[1]
#### 
#### p = subprocess.Popen("grep -A 1 \"print(result)\" " + filePath, stdout = subprocess.PIPE, shell=True)
#### (answer, err)  = p.communicate()
#### if "3565" in answer:
#### 	print 1
#### else: print 0


import os, sys, filecmp, re, shutil, time, subprocess, hashlib, os.path

class TestJob:
	jobCount = 0
	failCount = 0 
	passCount = 0	
	scriptCount = 0
	def __init__(self, pathToLL, pathToScripts, job, program):
		self.program = program
		self.pathToLL = pathToLL
		self.job = job
		self.pathToScripts = pathToScripts
		TestJob.jobCount += 1
		self.testScripts = []
		self.scriptResults = []

	def addTestScript(self, testScript): 
		self.testScripts.append(testScript)
		TestJob.scriptCount += 1

	def addScriptResult(self, result): self.scriptResults.append(result)
	def setLocalPath(self, localPath): self.localPath = localPath
	def setLocalLL(self, localLL): self.localLL = localLL
	def setID(self, ID): self.ID = ID
	def writeReport(self, report): self.report = report
	def writeScriptReport(self, report): self.scriptReport = report



# crawl through applications directory searching appropriate jobs files
# a job is appropriate if:
	# it is in the applications folder
	# it has path and extension of form: /applications/<program>/jobs/<jobname>/__.ll
	# it has at least one test script in the corresponding /applications/<program>/tests/<jobname>/scripts/__.py

# for ease of use within existing applications directory, scripts must also have LL within their name

def setupMiscTests():
	miscProgs = os.path.join(currDir, "miscProgs")
	tempDirList = []
	if os.path.isdir(miscProgs):
		for programDir in os.listdir(miscProgs):	
			os.system("cp -r miscProgs/" + programDir + " ../" + "misc" + programDir)
			tempDirList.append("../" + "misc" + programDir)
	return tempDirList

def findJobs():
	listOfJobs = []
	listOfLLs = []	
	for root, dir, files in os.walk(applicationsDir):
		for file in files:
			if os.path.splitext(file)[1] == ".ll":	
				# ensure .ll file is intended as a job
				if "/jobs/" in root:
					if not "/miscProgs/" in root:
						listOfLLs.append([root, file])
		# ensure .ll file has corresponding test script
	for pathInfo in listOfLLs:
		LLfile = pathInfo[0]
		scriptsDir = LLfile.replace('jobs', 'tests', 1)
		scriptsDir = os.path.join(scriptsDir, 'scripts')
		if os.path.isdir(scriptsDir):
			if os.listdir(scriptsDir) != []:	
				program = scriptsDir.replace(applicationsDir +"/", "")
				program = program.split("/")[0]
				
				
				for testScript in os.listdir(scriptsDir):
					if "py" and "LL" in testScript:
						newJob = TestJob(LLfile, scriptsDir, pathInfo[1], program)	
						newJob.addTestScript(testScript)	
						listOfJobs.append(newJob)	
	return listOfJobs			

# create local copies of jobs, and modifies their output paths					
def copyAndModifyJobs(listOfJobs):
	for job in listOfJobs:
		jobName = job.job
		localLoc = os.path.join(localJobsDir, job.program)
		pathToFile = os.path.join(job.pathToLL, jobName)
		shutil.copyfile(pathToFile, localLoc + "job.ll") # rename for duplicate .ll names
		filesDir = os.path.join(job.pathToLL, "files")
		if os.path.isdir(filesDir):
			if os.listdir(filesDir) != []:
				for myfile in os.listdir(filesDir):
					if not os.path.isdir(myfile):
						filePath = os.path.join(filesDir, myfile)
						shutil.copyfile(filePath, localJobsDir + "/" + myfile)
		job.setLocalLL(localLoc + "job.ll")		
		jobPath = localLoc + "job.ll"
		job.setLocalPath(jobPath)
		f = open(jobPath, 'r+b')
		fText = f.read()
		fText = re.sub('#@ initialdir.*', "#@ initialdir = " + currDir + "/localJobs", fText)
		fText = re.sub('#@ output.*', "#@ output = ../actualOutput/" + jobName[0:len(jobName)-3] + ".txt", fText)
		fText = re.sub('#@ error.*', "#@ error = ../errors/" + jobName[0:len(jobName)-3] + ".txt", fText)
		f.seek(0)	# seek and truncate needed or just appends new lines to bottom
		f.truncate()
		f.write(fText)
		f.close()
	
		

def LLsubmit(jobsList):
	for job in jobsList:
		testFile = job.localLL			
		p = subprocess.Popen("llsubmit " + testFile , stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
		(LLout, err)  = p.communicate()
	###	LLout = "llsubmit: The job \"login1-p.1259108\" has been submitted."
		if 'submitted' in LLout:
			jobId = LLout[19:35]
		else: 	
			jobId = "SUBMITFAILED"
		#print jobId
		job.setID(jobId)


# wait for job completion and output file writing
# naive MD5 hash of files for test success
def processOutput(jobsList):
	for job in jobsList:
		if job.ID == "SUBMITFAILED":
			job.writeReport("Submission to LL failed")
			break
		#p = subprocess.Popen("/share/bin/llwait " + job.ID, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
		#(completed, err) = p.communicate()
		os.system("/share/bin/llwait " + job.ID)	

	for job in jobsList: 
		actualFile = os.path.join(actualOutputDir, job.job[0:len(job.job)-3] + ".txt")
		acc = 0
		while not (os.path.isfile(actualFile)):
			acc = acc + 2			
			time.sleep(2)
			if (acc > 5):
				print("waiting on job: " + job.program)
				os.system("llq -u " + userId)
				acc = 0	
		#time.sleep(4)
		if (os.path.isfile(actualFile)):
			expectedFile = os.path.join(expectedOutputDir, job.job[0:len(job.job)-3] + "out.txt")
			
			if os.path.isfile(expectedFile):
				# get MD5 hash for actual and expected outputs, compare
				acF = open(actualFile)
				exF = open(expectedFile)
				acFtext = acF.read()
				exFtext = exF.read()
				acHash = hashlib.md5()
				acHash.update(acFtext)
				exHash = hashlib.md5()
				exHash.update(exFtext)
				acF.close()
				exF.close()

				if not (exHash.digest() == acHash.digest()):
		#		if not (filecmp.cmp(actualFile, expectedFile)):
					# files not equal, update report
					job.writeReport("test case " + job.program + " failed!")
				else:
					# files equal, update report
					job.writeReport("test case " + job.program + " successful!")
			else:
					# no expected output file was found, create and update
				os.system("touch " + expectedFile)	
				shutil.copyfile(actualFile, expectedFile)
				job.writeReport("no expected output for " + job.program + ", created by assuming current output is correct")
		else: 
				# odd case, should not occur?
			job.writeReport("LL job finished but no output? " + job.program)



def writeReportFile(jobsList):
	if os.path.isfile("fileReport.txt"):
		os.system("rm fileReport.txt")
	os.system("touch fileReport.txt")

	wholeReport = ""
	for job in jobsList:
		wholeReport = wholeReport + job.report + "\r\n"
	reportFile = os.path.join(currDir, "fileReport.txt")
	f = open(reportFile, 'r+b')
	f.write("programs tested: " + str(TestJob.jobCount) + "\r\n" + " used hash of LL job stdout for comparision, not reliable \r\n" + wholeReport)
	f.close()


def runTests(jobsList):
	for job in jobsList:
		for script in job.testScripts:
			scriptPath = os.path.join(job.pathToScripts, script)
			actualFile = os.path.join(actualOutputDir, job.job[0:len(job.job)-3] + ".txt")
			proc = subprocess.Popen("python " + scriptPath + " " + actualFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			err = ""
			(answer, err) = proc.communicate()
			#print answer
			answer = answer.strip()
			if (answer=="1") or (answer.upper()=="TRUE") or (answer==1):
				job.addScriptResult(job.program + " script " +  script + ": successful")
			elif (answer=="0") or (answer.upper()=="FALSE") or (answer==0):
				job.addScriptResult(job.program + " script " +  script + ": failed")
			else:
				job.addScriptResult(job.program + " script " + script + ": script output unexpected: " + answer[1:30] + ", err: " + err) #[1:30])
	
def writeScriptReport(jobsList):		
	if os.path.isfile("testReport.txt"):
		os.system("rm testReport.txt")
	os.system("touch testReport.txt")

	wholeReport = ""
	for job in jobsList:
		for result in job.scriptResults:
			wholeReport = wholeReport + result + "\r\n"

	reportFile = os.path.join(currDir, "testReport.txt")
	f = open(reportFile, 'r+b')
	f.write("programs tested: " + str(TestJob.jobCount) + "\r\n scripts tested: "+ str(TestJob.scriptCount) + "\r\n" + wholeReport)
	f.close()
	os.system("cat " + reportFile)




### script must be ran from a folder within the applications directory
# can change to find apps
p = subprocess.Popen("pwd", stdout = subprocess.PIPE, shell=True)
(currDir, err)  = p.communicate()
currDir = currDir.strip()

p1 = subprocess.Popen("id", stdout = subprocess.PIPE, shell=True)
(userId, er1) = p1.communicate()
userId = userId[9:16]  # probably not general enough

# set up directory paths
applicationsDir = os.path.join(currDir, "..")
localJobsDir = os.path.join(currDir, "localJobs")
actualOutputDir = os.path.join(currDir, "actualOutput/")
expectedOutputDir = os.path.join(currDir, "expectedOutput/")
testResultsDir = os.path.join(currDir, "testResults/")

errors = os.path.join(currDir, "errors/")

# for quick tests, allow grouping within ./miscProgs

tempDirList = setupMiscTests()

os.system("mkdir -p localJobs actualOutput expectedOutput errors")
os.system("rm -f " + actualOutputDir + "*.txt")



jobsList = findJobs()
copyAndModifyJobs(jobsList)
LLsubmit(jobsList)
processOutput(jobsList)
writeReportFile(jobsList)


runTests(jobsList)
writeScriptReport(jobsList)

for dir in tempDirList:
	os.system("rm -r " + dir)

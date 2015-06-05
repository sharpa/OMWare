# Module: Assemble.BioNano.BNGSummarize
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/04/2015
# 
# The purpose of this module is to WRITE CODE that will wait 
# until all jobs of a certain step are complete,
# then summarize them in a list file
from Operations.Step import Step

class Summarize(Step):
	def __init__(self, workspace, step):
		self.workspace=workspace
		self.step=step

	def writeCode(self):
		self.fetchPrereqs()

		code = "wd=`pwd`\n"
		code += "rm -f " + self.step.getListFile() + "\n"
		code += "let errors=0\n"
		code += "let total=0\n"
		code += "for output_file in " + self.getStepDir() + "/*.stdout\n"
		code += "do\n"
		code += "  let total+=1\n"
		code += "  result=`tail -n 1 $output_file`\n"
		code += "  if [[ $result != \"END of output\" ]]; then let errors+=1\n"
		code += "  else echo $wd/$file >> " + self.step.getListFile() + "; fi\n"
		code += "done\n"
		code += "if [ $total -ne " + str(self.step.total_job_count) + " ]; then let errors+=1; fi\n"

		code += "if [ $errors -ne 0 ]; then exit 1; fi\n"

		return [code]

	def getStepDir(self):
		return self.step.getStepDir()
	def fetchPrereqs(self):
		self.prereqs=[self.step]

	def getMem(self):
		return self.workspace.resources.getSmallMemory()
	def getTime(self):
		return self.workspace.resources.getSmallTime()
	def getThreads(self):
		return 1

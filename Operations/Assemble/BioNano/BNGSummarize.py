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

		self.autoGeneratePrereqs()

	def writeCode(self):

		code = "wd=`pwd`\n"
		code += "rm -f " + self.step.getListFile() + "\n"
		code += "let errors=0\n"
		code += "let total=0\n"
		code += "for stdout_file in " + self.getStepDir() + "/*.stdout\n"
		code += "do\n"
		code += "  let total+=1\n"
		code += "  result=`tail -n 1 $stdout_file`\n"
		code += "  if [[ $result != \"END of output\" ]]; then let errors+=1\n"
		code += "  else\n"
		code += "    file=`echo $stdout_file | sed 's/\.stdout/\." + self.step.getOutputFileExtension() + "/'`\n"
		code += "    echo $wd/$file >> " + self.step.getListFile() + ";\n"
		code += "  fi\n"
		code += "done\n"
		code += "if [ $total -ne " + str(self.step.total_job_count) + " ]; then let errors+=1; fi\n"

		code += "if [ $errors -ne 0 ]; then exit 1; else touch " + self.getStepDir() + "/Complete.status; fi\n"

		return [code]

	def getStepDir(self):
		return self.step.getStepDir()
	def autoGeneratePrereqs(self):
		pass
	def getPrereqs(self):
		return [self.step]
	def getOutputFileExtension(self):
		return "list"

	def getMem(self):
		return self.workspace.resources.getSmallMemory()
	def getTime(self):
		return self.workspace.resources.getSmallTime()
	def getThreads(self):
		return 1


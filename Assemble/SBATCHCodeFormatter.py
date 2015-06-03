# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/03/2015
# 
# The purpose of this module is take as input "code" for a code generator (step)
# class, and format it for a specific platform, namely SBATCH
import Assemble.CodeFormatter

class CodeFormatter (Assemble.CodeFormatter.CodeFormatter):
	def __init__(self):
		pass
	def formatCode(self, step):
		
		prereqs=step.getPrereqs()
		for prereq in prereqs:
			self.formatCode(prereq)
		
		for part in step.writeCode():
			print("#!/bin/bash")
			print("#SBATCH --mem " + str(1024*step.getMem()) + "M")
			print("#SBATCH --time " + str(step.getTime()) + ":00:00")
			print("#SBATCH --ntasks " + str(step.getThreads()))
			print(part)

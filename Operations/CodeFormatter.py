# Module: Operations.CodeFormatter
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/02/2015
# 
# The purpose of this module is take as input "code" for a code generator
# class, and format it for a specific platform, such as SBATCH

class CodeFormatter:
	def __init__(self):
		pass

	def formatCode(self, step):
		raise Exception("Abstract method called")
	def runOneStep(self, step):
		raise Exception("Abstract method called")
	def runSeveralSteps(self, tree): 
		raise Exception("Abstract method called")

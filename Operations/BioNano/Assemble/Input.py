# Module: Operations.BioNano.Assemble.Input
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# encapsulate the initial input .bnx file of a BNG assembly
from Operations.Step import Step
from os import path

class Input(Step):
	def __init__(self, workspace):
		self.workspace=workspace
	def __hash__(self):
		return hash((self.workspace.input_file, self.workspace.work_dir, self.__class__.__name__))

	def writeCode(self):
		return []

	def getStepDir(self):
		return self.workspace.input_file

	def getOutputFile(self):
		return self.workspace.input_file

	def getOutputFileExtension(self):
		return self.bnx_file.getExtension()

	def autoGeneratePrereqs(self):
		pass
	def getPrereqs(self):
		return []

	def isComplete(self):
		return path.exists(self.getOutputFile())

	def getMem(self):
		return -1
	def getTime(self):
		return -1
	def getThreads(self):
		return -1

# Module: Operations.BioNano.Compare.Input
# Version: 0.1
# Author: Aaron Sharp
# Date: 08/24/2015
# 
# The purpose of this module is to encapsulate an input file (.cmap) for optical map comparisons
from Operations.Step import Step

class Input(Step):
	def __init__(self, workspace):
		self.workspace=workspace
		self.quality=None
	def __hash__(self):
		return hash((self.workspace.input_file, self.workspace.work_dir, self.__class__.__name__))

	def __eq__(self, other):
		if other is None:
			return False
		if self.__class__ != other.__class__:
			return False
		return self.workspace==other.workspace
	def __ne__(self, other):
		return not self == other

	def __str__(self):
		return "Input: " + self.workspace.input_file

	def writeCode(self):
		return []
	def getStepDir(self):
		return self.workspace.input_file
	def getOutputFile(self):
		return self.workspace.input_file
	def getOutputFileExtension(self):
		return CmapFile.getExtension()
	def autoGeneratePrereqs(self):
		pass
	def getPrereq(self):
		return None

	def getMem(self):
		return -1
	def getTime(self):
		return -1
	def getThreads(self):
		return -1

from Operations.BioNano.files import CmapFile

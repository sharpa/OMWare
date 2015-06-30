# Module: Operations.Step
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/01/2015
# 
# The purpose of this module is abstractify code generator step classes
from os import path

class Step(object):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters

		self.autoGeneratePrereqs()

	def __hash__(self):
		return hash((self.workspace.input_file, self.workspace.work_dir, self.vital_parameters.pval, self.vital_parameters.fp, self.vital_parameters.fn, self.vital_parameters.min_molecule_len, self.vital_parameters.min_molecule_sites, self.__class__.__name__))
		
	def __eq__(self, other):
		return self.__dict__ == other.__dict__
	def __ne__(self, other):
		return not self == other
	def __str__(self):
		return str(self.vital_parameters.__dict__)

	def writeCode(self):
		raise Exception("Abstract method called")

	def getStepDir(self):
		raise Exception("Abstract method called")

	def getOutputFileExtension(self):
		raise Exception("Abstract method called")

	def autoGeneratePrereqs(self):
		raise Exception("Abstract method called")

	def getPrereqs(self):
		raise Exception("Abstract method called")

	def isComplete(self):
		return path.exists(self.getStepDir() + "/Complete.status")

	def getMem(self):
		raise Exception("Abstract method called")
	def getTime(self):
		raise Exception("Abstract method called")
	def getThreads(self):
		raise Exception("Abstract method called")

	def getErrorNotificationEmail(self):
		return self.workspace.errorNotificationEmail

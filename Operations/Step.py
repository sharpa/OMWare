# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/01/2015
# 
# The purpose of this module is abstractify code generator step classes

class Step(object):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters

	def writeCode(self):
		raise Exception("Abstract method called")

	def getStepDir(self):
		raise Exception("Abstract method called")

	def fetchPrereqs(self):
		raise Exception("Abstract method called")

	def getPrereqs(self):
		self.fetchPrereqs()
		return self.prereqs

	def isComplete(self):
		return False

	def getMem(self):
		raise Exception("Abstract method called")
	def getTime(self):
		raise Exception("Abstract method called")
	def getThreads(self):
		raise Exception("Abstract method called")

	def getErrorNotificationEmail(self):
		return self.workspace.errorNotificationEmail

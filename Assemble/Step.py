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
		pass

	def writePrereqCode(self):
		self.fetchPrereqs()
		for step in self.prereqs:
			if not step.isComplete():
				step.writeCode()

	def getStepDir(self):
		pass

	def fetchPrereqs(self):
		pass

	def isComplete(self):
		return False

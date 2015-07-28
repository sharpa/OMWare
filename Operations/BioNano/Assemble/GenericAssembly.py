# Module: Operations.BioNano.Assemble.GenericAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 07/27/2015
# 
# The purpose of this module is to abstractify several different steps that could all accurately be called "Assemblies"
from Operations.Step import Step

class GenericAssembly(Step):
	def __init__(self, workspace, vital_parameters):
		raise Exception("Abstract method called")
	def writeCode(self):
		raise Exception("Abstract method called")

	def getStepDir(self):
		raise Exception("Abstract method called")

	def getOutputFile(self):
		return self.getStepDir() + "/" + self.output_prefix + "." + self.getOutputFileExtension()

	def getOutputFileExtension(self):
		return "contigs"

	def autoGeneratePrereqs(self):
		raise Exception("Abstract method called")

	def getPrereq(self):
		raise Exception("Abstract method called")

	def getMem(self):
		raise Exception("Abstract method called")

	def getTime(self):
		raise Exception("Abstract method called")
	
	def getThreads(self):
		raise Exception("Abstract method called")

	@staticmethod
	def createAssembly(workspace, vital_parameters, assembly_type):
		if assembly_type=="assembly":
			return Operations.BioNano.Assemble.Assembly.Assembly(workspace, vital_parameters)
		if assembly_type=="refineA":
			return Operations.BioNano.Assemble.RefineA.RefineA(workspace, vital_parameters)

import Operations.BioNano.Assemble.Assembly
import Operations.BioNano.Assemble.RefineA

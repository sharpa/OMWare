# Module: Operations.Step
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/01/2015
# 
# The purpose of this module is abstractify code generator step classes
from os import path
import json

class Step(object):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters
		self.quality=None

		self.autoGeneratePrereqs()

	def __hash__(self):
		return hash((self.workspace.input_file, self.workspace.work_dir, self.vital_parameters.pval, self.vital_parameters.fp, self.vital_parameters.fn, self.vital_parameters.min_molecule_len, self.vital_parameters.min_molecule_sites, self.__class__.__name__))
		
	def __eq__(self, other):
		return self.__dict__ == other.__dict__
	def __ne__(self, other):
		return not self == other
	def __str__(self):
		return str(self.vital_parameters.__dict__)

	@staticmethod
	def generateFromStepDir(step_dir):
		raise Exception("Abstract method called")

	def writeCode(self):
		raise Exception("Abstract method called")

	def getStepDir(self):
		raise Exception("Abstract method called")

	def getOutputFile(self):
		raise Exception("Abstract method called")

	def getOutputFileExtension(self):
		raise Exception("Abstract method called")

	def autoGeneratePrereqs(self):
		raise Exception("Abstract method called")

	def getPrereq(self):
		raise Exception("Abstract method called")

	def isComplete(self):
		return path.exists(self.getStepDir() + "/Complete.status")

	def getQualityFileName(self):
		return self.getStepDir() + "/Quality.json"

	def loadQualityReport(self, log_level):
		if self.quality is None:
			self.loadQualityObjectFromFile()

		qualityReportItems=[]
		allQualityReportItems=self.loadQualityReportItems()
		for item in allQualityReportItems.keys():
			if allQualityReportItems[item] <= log_level:
				qualityReportItems.append(item)

		return qualityReportItems

	def loadQualityReportItems(self):
		raise Exception("Abstract method called")

	def createQualityObject(self):
		raise Exception("Abstract method called")

	def saveQualityObjectToFile(self):
		if self.quality is None:
			self.createQualityObject()
		with open(self.getQualityFileName(), "w") as quality_file:
			json.dump(self.quality.__dict__, quality_file, indent=1)

	def loadQualityObjectFromFile(self):
		if not path.exists(self.getQualityFileName()):
			self.createQualityObject()
		with open(self.getQualityFileName()) as quality_file:
			self.quality=Quality()
			self.quality.__dict__=json.load(quality_file)

	def getMem(self):
		raise Exception("Abstract method called")
	def getTime(self):
		raise Exception("Abstract method called")
	def getThreads(self):
		raise Exception("Abstract method called")

	def getErrorNotificationEmail(self):
		return self.workspace.errorNotificationEmail

class Quality(object):
	def __init__(self, **kwards):
		self.__dict__.update(kwards)
	def __eq__(self, other):
		if other is None:
			return False
		return self.__dict__ == other.__dict__
	def __str__(self):
		return str(self.__dict__)

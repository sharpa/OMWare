# Module: Operations.BioNano.Compare.Input
# Version: 0.1
# Author: Aaron Sharp
# Date: 08/24/2015
# 
# The purpose of this module is to encapsulate an input file (.cmap) for optical map comparisons
from Operations.Step import Step
from os import path

class Input(Step):
	def __init__(self, workspace):
		self.workspace=workspace
		file_data=self.workspace.input_file.split('/')
		self.file_name=file_data[len(file_data)-1]
		self.prereq=None
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
		code="cd " + self.workspace.work_dir + "\n"
		code+="mkdir " + self.getStepDir() + "\n"
		code+="cd " + self.getStepDir() + "\n"
		code+="pwd\n"

		code+="ln -s ../" + self.workspace.input_file + " " + self.file_name + "\n"
		code+="if [ $? -eq 0 ]; then touch Complete.status; fi;\n"
		return [code]

	def getStepDir(self):
		return "comparison_input_" + self.file_name
	def getOutputFile(self):
		return self.getStepDir() + "/" + self.file_name
	def getOutputFileExtension(self):
		return CmapFile.getExtension()
	def autoGeneratePrereqs(self):
		pass
	def getPrereq(self):
		return self.prereq

	def getCmapFile(self):
		return CmapFile(self.getOutputFile())

	def loadQualityReportItems(self):
		if self.quality is None:
			self.loadQualityObjectFromFile()
		return {"Length: " + str(self.quality.length): 1}

	def createQualityObject(self):
		if not self.isComplete():
			raise Exception("Quality cannot be determined before step is complete")
		length=0
		ids=set()
		for label in self.getCmapFile().parse():
			if label.contig_id not in ids:
				length+=label.contig_len
				ids.add(label.contig_id)
		self.quality=Quality(length=length)
		self.saveQualityObjectToFile()

	def loadQuality_length(self):
		if self.quality is None:
			self.loadQualityObjectFromFile()
		return self.quality.length

	def getMem(self):
		return 1
	def getTime(self):
		return 1
	def getThreads(self):
		return 1

from Operations.BioNano.files import CmapFile
from Operations.Step import Quality

# Module: Operations.BioNano.Assemble.Input
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# encapsulate the initial input .bnx file of a BNG assembly
from Operations.Step import Step
from Operations.Step import Quality
from Operations.BioNano.file_bnx import BnxFile
from os import path
from collections import OrderedDict

class Input(Step):
	def __init__(self, workspace):
		self.workspace=workspace
		self.quality=None
	def __hash__(self):
		return hash((self.workspace.input_file, self.workspace.work_dir, self.__class__.__name__))

	def writeCode(self):
		return []

	def getStepDir(self):
		return self.workspace.input_file

	def getOutputFile(self):
		return self.workspace.input_file

	def getOutputFileExtension(self):
		return BnxFile.getExtension()

	def autoGeneratePrereqs(self):
		pass
	def getPrereqs(self):
		return []

	def isComplete(self):
		return path.exists(self.getOutputFile())

	def getBnxFile(self):
		return BnxFile(self.workspace.input_file)

	def createQualityObject(self):
		count=0
		quantity=0.0
		labels=0
		for molecule in self.getBnxFile().parse('bnx'):
			count+=1
			quantity+=molecule.length
			labels+=molecule.num_labels

		self.quality=Quality(count=count, quantity=quantity, labels=labels)
		self.saveQualityObjectToFile()

	def loadQualityReportItems(self):
		report_items=OrderedDict()
		report_items["File: " + str(self.getOutputFile())]=3
		report_items["Molecule count: " + str(self.loadQuality_count())]=1
		report_items["Total quantity: " + str(self.loadQuality_quantity())]=1
		report_items["Total labels: " + str(self.loadQuality_labels())]=1
		report_items["Average label density: " + str(self.loadQuality_density())]=2
		report_items["Average length: " + str(self.loadQuality_averageLength())]=2
		return report_items

	def loadQuality_count(self):
		if self.quality is None:
			self.createQualityObject()
		return self.quality.count

	def loadQuality_quantity(self):
		if self.quality is None:
			self.createQualityObject()
		return self.quality.quantity
	def loadQuality_labels(self):
		if self.quality is None:
			self.createQualityObject()
		return self.quality.labels
	def loadQuality_density(self):
		if self.quality is None:
			self.createQualityObject()
		density=0.0
		try:
			density=self.quality.density
		except AttributeError:
			density=self.quality.labels/self.quality.quantity
			self.quality.density=density
		return density
	def loadQuality_averageLength(self):
		if self.quality is None:
			self.createQualityObject()
		average=0.0
		try:
			average=self.quality.average
		except AttributeError:
			average=self.quality.quantity/self.quality.count
			self.quality.average=average
		return average

	def getMem(self):
		return -1
	def getTime(self):
		return -1
	def getThreads(self):
		return -1

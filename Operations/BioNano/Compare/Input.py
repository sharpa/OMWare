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
#		return self.step_dir
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
		return {"Length: " + str(self.quality.length): 1,
			"Count: " + str(self.quality.count): 1,
			"N50: " + str(self.quality.n50): 2}

	def createQualityObject(self):
		if not self.isComplete():
			raise Exception("Quality cannot be determined before step is complete")
		lengths=[]
		total_length=0
		ids=set()
		max_coverage=-1
		min_max_coverage=-1
		for label in self.getCmapFile().parse():
			if label.contig_id not in ids:
				if max_coverage < min_max_coverage or min_max_coverage < 0:
					min_max_coverage=max_coverage
				max_coverage=0.0
				lengths.append(label.contig_len)
				total_length+=label.contig_len
				ids.add(label.contig_id)
			if label.coverage > max_coverage:
				max_coverage=label.coverage
			

		sorted_lengths=sorted(lengths, reverse=True)
		minlen=sorted_lengths[len(sorted_lengths)-1]
		maxlen=sorted_lengths[0]
		n50=0
		length_included_in_n50=0
		target_length_included=float(total_length)/2.0
		for length in sorted_lengths:
			length_included_in_n50+=length
			if length_included_in_n50 >= target_length_included:
				n50=length
				break

		self.quality=Quality(length=total_length, count=len(ids), average_length=total_length/count, n50=n50, min=minlen, max=maxlen, min_max_coverage=min_max_coverage)
		self.saveQualityObjectToFile()

	def loadQuality_length(self):
		if self.quality is None:
			self.loadQualityObjectFromFile()
		return self.quality.length

	def loadQuality_count(self):
		if self.quality is None:
			self.loadQualityObjectFromFile()
		return self.quality.count

	def getMem(self):
		return 1
	def getTime(self):
		return 1
	def getThreads(self):
		return 1

from Operations.BioNano.files import CmapFile
from Operations.Step import Quality

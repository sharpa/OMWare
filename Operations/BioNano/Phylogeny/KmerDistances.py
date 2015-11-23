class KmerDistances(Step):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters
		self.autoGeneratePrereqs()
	def __hash__(self):
		return hash((self.workspace.input_file, self.workspace.work_dir, self.vital_paraemters.k, self.__class__.__name__))

	def writeCode(self):
		pass #

	def calculateDistances(self):
		with open(self.workspace.input_file) as i_file:
			for line in i_file:
				
		
	def getStepDir(self):
		return "_".join(["kmers", self.workspace.input_file, self.vital_parameters.k])
	def getOutputFile(self):
		return self.getStepDir() + "/" + self.getOutputFile()
	def getOutputFileExtension(self):
		return "nex"
	def autoGeneratePrereqs(self):
		pass
		#Input
	def getPrereq(self):
		pass
		#Input
	def loadQualityReportItems(self):
		pass #
	def createQualityObject(self):
		pass #
	def getMem(self):
		return 1
	def getTime(self):
		return 1
	def getThreads(self):
		return 1

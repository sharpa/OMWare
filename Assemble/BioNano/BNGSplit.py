# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# split a single bnx file into "good sized" chunks of molecules
# for more efficient parallel assembly
from Assemble.Step import Step
from Assemble.BioNano.BNGSort import Sort
import math
from collections import OrderedDict

class Split(Step):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters

		self.overwrite_output=True
		self.send_output_to_file=True
		self.send_error_to_file=True

		with open(self.workspace.work_dir + "/" + self.workspace.input_file) as iFile:
			count=0
			site_count=0
			for line in iFile:
				if line[0] == "0":
				    count+=1
				if line[0] == "1":
				    site_count+=len(line.split())-1

			blocks=int(math.ceil(count/80000.0))
			site_blocks=int(math.ceil(site_count/1e6))
			if site_blocks>blocks:
				blocks=site_blocks
			self.block_count=blocks

	def writeCode(self):
		self.writePrereqCode()

		print("cd " + self.workspace.work_dir)
		print("mkdir -p " + self.getStepDir())
		print("cd " + self.getStepDir())

		param_values=OrderedDict()
		param_values["-i"] =  self.sort.getOutputFile()
		param_values["-maxthreads"] =  str(self.workspace.resources.getMaxThreads())
		param_values["-merge"] =  ""
		param_values["-bnx"] =  ""

		if self.overwrite_output:
			param_values["-f"] = ""
		if self.send_output_to_file:
			param_values["-stdout"] = ""
		if self.send_error_to_file:
			param_values["-stderr"] = ""

		i=1
		while i <= self.block_count:
			param_list=[self.workspace.binaries["bng_ref_aligner"]]
			param_values["-o"]="split_" + str(i) + "_of_" + str(self.block_count)
			param_values["-subsetbin"]=str(i) + " " + str(self.block_count)
			for key in param_values:
				param_list.append(key)
				param_list.append(param_values[key])
			print(" ".join(param_list))
			i+=1

	def getListFile(self):
		return "split.list"

	def getStepDir(self):
		return "_".join(["split", self.workspace.input_file, "blockCount"+str(self.block_count)])

	def fetchPrereqs(self):
		self.sort=Sort(self.workspace, self.vital_parameters)
		self.prereqs=[self.sort]




	def getBlock(self, block_num):
		return "split_" + str(block_num) + "_of_" + str(self.block_count) + ".bnx"

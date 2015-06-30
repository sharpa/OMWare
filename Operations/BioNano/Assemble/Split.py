# Module: Operations.BioNano.Assemble.Split
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# split a single bnx file into "good sized" chunks of molecules
# for more efficient parallel assembly
from Operations.Step import Step
from Operations.BioNano.Assemble.Sort import Sort
import math
from collections import OrderedDict

class Split(Step):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters

		self.overwrite_output=True
		self.send_output_to_file=True
		self.send_error_to_file=True

		if vital_parameters.blocks is None:
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
				self.total_job_count=blocks
				self.vital_parameters.blocks=blocks
		else:
			self.total_job_count=vital_parameters.blocks

		self.max_job_count=self.getTime()*(60/5)-3
		if self.max_job_count<1:
			self.max_job_count=1

		self.autoGeneratePrereqs()

	def writeCode(self):
		code_parts=[]

		param_values=OrderedDict()
		param_values["-i"] =  "../" + self.sort.getOutputFile()
		param_values["-o"] =  "placeholder"
		param_values["-maxthreads"] =  str(self.getThreads())
		param_values["-merge"] =  ""
		param_values["-bnx"] =  ""

		if self.overwrite_output:
			param_values["-f"] = ""
		if self.send_output_to_file:
			param_values["-stdout"] = ""
		if self.send_error_to_file:
			param_values["-stderr"] = ""

		tmp_code=""
		cur_jobs=0
		for cur_block in xrange(1, self.total_job_count+1):
			param_list=[self.workspace.binaries["bng_ref_aligner"]]
			param_values["-o"]="split_" + str(cur_block) + "_of_" + str(self.total_job_count)
			param_values["-subsetbin"]=str(cur_block) + " " + str(self.total_job_count)
			for key in param_values:
				param_list.append(key)
				param_list.append(param_values[key])

			tmp_code += " ".join(param_list) + "\n"
			cur_jobs+=1

			if cur_jobs>=self.max_job_count or cur_block==self.total_job_count:
				code = "cd " + self.workspace.work_dir + "\n"
				code += "mkdir -p " + self.getStepDir() + "\n"
				code += "cd " + self.getStepDir() + "\n"
				code += tmp_code
				code += "pwd\n"

				code_parts.append(code)

				cur_jobs=0
				tmp_code=""

		return code_parts

	def getListFile(self):
		return self.getStepDir() + "/split.list"

	def getStepDir(self):
		return "_".join(["split", self.workspace.input_file, "blockCount"+str(self.total_job_count)])

	def autoGeneratePrereqs(self):
		self.sort=Sort(self.workspace, self.vital_parameters)

	def getPrereqs(self):
		return [self.sort]


	def getMem(self):
		return self.workspace.resources.getMediumMemory()
	def getTime(self):
		return self.workspace.resources.getSmallTime()
	def getThreads(self):
		return self.workspace.resources.getSmallThreads()

	def getOutputFile(self, block_num):
		return self.getStepDir() + "/split_" + str(block_num) + "_of_" + str(self.total_job_count) + ".bnx"
	def getOutputFileExtension(self):
		return "bnx"

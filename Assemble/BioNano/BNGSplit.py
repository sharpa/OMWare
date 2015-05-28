# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# split a single bnx file into "good sized" chunks of molecules
# for more efficient parallel assembly
import math
from Utils.MacbookProResources import MacbookProResources
from Assemble.BioNano.BNGSort import Sort

class Split:
	def __init__(self, input_file):
		self.input_file=input_file
		self.work_dir="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir"
		self.ref_aligner_bin="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_scratch_input/RefAligner"

		self.resources=MacbookProResources()

		# TODO initialize the value of blocks here instead of during print code
		self.blocks=10

		self.overwrite_output=True
		self.send_output_to_file=True
		self.send_error_to_file=True

		self.sort=Sort(input_file)

	def writeCode(self):
		param_values={
			"-i": self.sort.getSortedFile(),
			"-maxthreads": str(self.resources.getMaxThreads()),
			"-merge": "",
			"-bnx": "",
			"-o": "all_-999_of_-999",
			"-subsetbin": "-999 -999",
		}
		if self.overwrite_output:
			param_values["-f"] = ""
		if self.send_output_to_file:
			param_values["-stdout"] = ""
		if self.send_error_to_file:
			param_values["-stderr"] = ""

		with open(self.work_dir + "/" + self.input_file) as iFile:
			count=0
			site_count=0
			for line in iFile:
				if line[0] == "0":
				    count+=1
				if line[0] == "1":
				    site_count+=len(line.split())-1

			blocks=int(math.ceil(count/80000.0))
			self.blocks=blocks
			site_blocks=int(math.ceil(site_count/1e6))
			if site_blocks>blocks:
				blocks=site_blocks

			i=1
			while i <= blocks:
				param_list=[self.ref_aligner_bin]
				param_values["-o"]="all_" + str(i) + "_of_" + str(blocks)
				param_values["-subsetbin"]=str(i) + " " + str(blocks)
				for key in param_values:
					param_list.append(key)
					param_list.append(param_values[key])
				print(" ".join(param_list))
				i+=1
	def getBlockCount(self):
		return self.blocks
	def getBlock(self, block_num):
		return "all_" + str(block_num) + "_of_" + str(self.blocks) + ".bnx"
	def getListFile(self):
		return "all.list"

# Module: Operations.BioNano.Assemble.Merge
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# merge several consensus contig files (cmap) into one
from Operations.Step import Step
from collections import OrderedDict

class Merge(Step):
	def __init__(self, workspace, assembly):
		self.workspace=workspace
		self.assembly=assembly
		self.quality=assembly.quality

		self.output_prefix="merge_of_"+assembly.output_prefix
		self.overwrite_output=True
		self.write_output_to_file=True
		self.write_error_to_file=True

		self.autoGeneratePrereqs()

	def __eq__(self, other):
		if other is None:
			return False
		if self.__class__ != other.__class__:
			return False
		return self.assembly==other.assembly

	def __ne__(self, other):
		return not self==other

	def __str__(self):
		return "merge of " + str(self.assembly)
		
	def writeCode(self):
		code="cd " + self.workspace.work_dir + "\n"
		code+="mkdir -p " + self.getStepDir() + "\n"
		code+="cd " + self.getStepDir() + "\n"
		code+="pwd\n"

		param_values=OrderedDict()
		param_values["-if"]="../" + self.assembly_summary.getOutputFile()
		param_values["-merge"]=""
		param_values["-o"]=self.output_prefix
		if self.overwrite_output:
			param_values["-f"]=""
		if self.write_output_to_file:
			param_values["-stdout"]=""
		if self.write_error_to_file:
			param_values["-stderr"]=""
		
		param_list=[self.workspace.binaries["bng_ref_aligner"]]
		for key in param_values:
			param_list.append(key)
			param_list.append(param_values[key])

		code+=" ".join(param_list) + "\n"

		code += "result=`tail -n 1 ../" + self.getStepDir()  + "/" + self.output_prefix + ".stdout`\n"
		code += "if [[ \"$result\" != \"END of output\" ]]; then exit 1; else touch Complete.status; fi\n"

		return [code]

	def getStepDir(self):
		return "merged_" + self.assembly.getStepDir()
	def getOutputFile(self):
		return self.getStepDir() + "/" + self.output_prefix + "." + self.getOutputFileExtension()
	def getOutputFileExtension(self):
		return "cmap"
	def autoGeneratePrereqs(self):
		self.assembly_summary=Summarize(self.workspace, self.assembly)
	def getPrereq(self):
		return self.assembly_summary

	def getMem(self):
		return self.workspace.resources.getSmallMemory()
	def getTime(self):
		return self.workspace.resources.getSmallTime()
	def getThreads(self):
		return 1

from Operations.BioNano.Assemble.Summarize import Summarize

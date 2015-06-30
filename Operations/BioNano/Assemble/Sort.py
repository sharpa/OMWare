# Module: Operations.BioNano.Assemble.Assembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner and Assembler software to create sort an input dataset
from Operations.Step import Step
from Operations.BioNano.Assemble.Input import Input
from Operations.BioNano.Assemble.MoleculeStats import MoleculeStats
from collections import OrderedDict

class Sort(Step):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters

		self.output_prefix="sorted"
		self.min_snr=2
		self.overwrite_output=True
		self.send_output_to_file=True
		self.send_errors_to_file=True

		self.autoGeneratePrereqs()

	def writeCode(self):
		code = "cd " + self.workspace.work_dir + "\n"
		code += "mkdir -p " + self.getStepDir() + "\n"
		code += "cd " + self.getStepDir() + "\n"
		code += "pwd\n"

		param_values=OrderedDict()
		param_values["-i"] =  "../" + self.inpt.getOutputFile()
		param_values["-maxthreads"] =  str(self.getThreads())
		param_values["-merge"] =  ""
		param_values["-sort-idinc"] =  ""
		param_values["-bnx"] =  ""
		param_values["-o"] =  self.output_prefix
		param_values["-minlen"] =  str(self.vital_parameters.min_molecule_len)
		param_values["-minsites"] =  str(self.vital_parameters.min_molecule_sites)
		param_values["-minSNR"] =  str(self.min_snr)
		param_values["-XmapStatWrite"] =  "../" + self.molecule_stats.getOutputFile()

		if self.overwrite_output:
			param_values["-f"] = ""
		if self.send_output_to_file:
			param_values["-stdout"] = ""
		if self.send_errors_to_file:
			param_values["-stderr"] = ""
		
		param_list=[self.workspace.binaries["bng_ref_aligner"]]
		for key in param_values:
			param_list.append(key)
			param_list.append(param_values[key])
		code += " ".join(param_list) + "\n"

		code += "result=`tail -n 1 ../" + self.getStepDir()  + "/" + self.output_prefix + ".stdout`\n"
		code += "if [[ \"$result\" != \"END of output\" ]]; then exit 1; else touch Complete.status; fi\n"
		return [code]

	def getOutputFile(self):
		return self.getStepDir() + "/" + self.output_prefix + ".bnx"
	def getOutputFileExtension(self):
		return "bnx"

	def getStepDir(self):
		return "_".join(["sorted",self.inpt.getStepDir(), "minlen"+str(self.vital_parameters.min_molecule_len), "minsites"+str(self.vital_parameters.min_molecule_sites)])

	def autoGeneratePrereqs(self):
		self.inpt=Input(self.workspace)
		self.molecule_stats=self.getMoleculeStats()

	def getPrereqs(self):
		return [self.inpt]

	def getMem(self):
		return self.workspace.resources.getMediumMemory()
	def getTime(self):
		return self.workspace.resources.getSmallTime()
	def getThreads(sef):
		return 1



	def getMoleculeStats(self):
		return MoleculeStats(self.getStepDir())


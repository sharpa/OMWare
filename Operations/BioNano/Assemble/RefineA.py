# Module: Assemble.BioNano.RefineA
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/29/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the first step of BNG refinement

from Operations.Step import Step
from Operations.BioNano.Assemble.Input import Input
from Operations.BioNano.Assemble.Sort import Sort
from Operations.BioNano.Assemble.Split import Split
from Operations.BioNano.Assemble.PairwiseAlignment import PairwiseAlignment
from Operations.BioNano.Assemble.Assembly import Assembly
from Operations.BioNano.Assemble.GroupManifest import GroupManifest
from collections import OrderedDict
from copy import copy

class RefineA(Step):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters
		self.quality=None

		self.sd=0.2
		self.sf=0.2
		self.sr=0.03
		self.res=3.3
		self.usecolor=1
		self.use_multi_mode=True
		self.consensus_end_coverage=0.99
		self.bias_for_low_likelihood_ratio=1e2
		self.refinement_length_accuracy=""
		self.largest_query_map_interval=4
		self.largest_reference_map_interval=6
		self.outlier_pval=1e-5
		self.end_outlier_prior_probability=0.00001
		self.contigs_format=1
		self.overwrite_output=True
		self.output_prefix="refineeA"
		self.send_output_to_file=True
		self.send_errors_to_file=True

		self.autoGeneratePrereqs()

	def writeCode(self):
		code="cd " + self.workspace.work_dir + "\n"
		code+="mkdir " + self.getStepDir() + "\n"
		code+="cd " + self.getStepDir() + "\n"
		code+="pwd\n"

		param_values=OrderedDict()
		param_values["-i"]="../" + self.sort.getOutputFile()
		param_values["-contigs"]=" ".join(["../" + self.assembly.getOutputFile(), "$group_start", "$group_end"])
		param_values["-maxthreads"]=str(self.getThreads())
		param_values["-T"]=str(self.vital_parameters.pval)
		param_values["-usecolor"]=str(self.usecolor)
		param_values["-extend"]="1"
		param_values["-refine"]="2"
		if self.use_multi_mode:
			param_values["-MultiMode"]=""
		param_values["-EndTrim"]=str(self.consensus_end_coverage)
		param_values["-LRBias"]=str(self.bias_for_low_likelihood_ratio)
		param_values["-Mprobeval"]=str(self.refinement_length_accuracy)
		param_values["-deltaX"]=str(self.largest_query_map_interval)
		param_values["-deltaY"]=str(self.largest_reference_map_interval)
		param_values["-outlier"]=str(self.outlier_pval)
		param_values["-endoutlier"]=str(self.end_outlier_prior_probability)
		param_values["-contigs_format"]=str(self.contigs_format)
		if self.overwrite_output:
			param_values["-force"]=""
		param_values["-FP"]=str(self.vital_parameters.fp)
		param_values["-FN"]=str(self.vital_parameters.fn)
		param_values["-sd"]=str(self.sd)
		param_values["-sf"]=str(self.sf)
		param_values["-sr"]=str(self.sr)
		param_values["-res"]=str(self.res)
		param_values["-output_prefix"]=self.output_prefix
		if self.send_output_to_file:
			param_values["-stdout"]=""
		if self.send_errors_to_file:
			param_values["-stderr"]=""
		param_values["-XmapStatRead"]="../" + self.molecule_stats.getOutputFile()
		
		param_list=[self.workspace.binaries["bng_assembler"]]
		for key in param_values:
			param_list.append(key)
			param_list.append(param_values[key])

		code+="let contig_num=0\n"
		code+="while read line\n"
		code+="do\n"
		code+="  if [[ $line == \"#\"* ]]; then continue; fi\n"
		code+="  let contig_num+=1\n"
		code+="  group_start=`echo $line | awk '{print $2}'`\n"
		code+="  group_end=`echo $line | awk '{print $3}'`\n"
		code+="    " + " ".join(param_list) + "\n"
		code+="done < ../" + self.getPrereqs()[0].getOutputFile()

		return [code]
		
	def getStepDir(self):
		return "_".join(["refineA", self.inpt.getStepDir(), "fp"+str(self.vital_parameters.fp), "fn"+str(self.vital_parameters.fn), "pval"+str(self.vital_parameters.pval), "minlen"+str(self.vital_parameters.min_molecule_len), "minsites"+str(self.vital_parameters.min_molecule_sites)])

	def getOutputFile(self):
		return self.getStepDir() + "/" + self.output_prefix + "." + self.getOutputFileExtension()

	def getOutputFileExtension(self):
		return "contigs"

	def autoGeneratePrereqs(self):
		self.inpt=Input(self.workspace)
		self.sort=Sort(self.workspace, copy(self.vital_parameters))
		self.molecule_stats=self.sort.getMoleculeStats()
		self.split=Split(self.workspace, copy(self.vital_parameters))
		self.pairwise_alignment=PairwiseAlignment(self.workspace, copy(self.vital_parameters))
		self.assembly=Assembly(self.workspace, copy(self.vital_parameters))
	def getPrereqs(self):
		return [GroupManifest(self.workspace, self.assembly)]

	def getMem(self):
		return self.workspace.resources.getMediumMemory()
	def getTime(self):
		return self.workspace.resources.getLargeTime()
	def getThreads(self):
		return self.workspace.resources.getMediumThreads()

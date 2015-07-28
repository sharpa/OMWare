# Module: Operations.BioNano.Assemble.Assembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner and Assembler software to create an optical map de novo assembly
from Operations.Step import Step
from collections import OrderedDict
from copy import copy

class GenericAssembly(Step):
	def __init__(self, workspace, vital_parameters):
		raise Exception("Abstract method called")
	def writeCode(self):
		raise Exception("Abstract method called")

	def getStepDir(self):
		raise Exception("Abstract method called")

	def getOutputFile(self):
		return self.getStepDir() + "/" + self.output_prefix + "." + self.getOutputFileExtension()

	def getOutputFileExtension(self):
		return "contigs"

	def autoGeneratePrereqs(self):
		raise Exception("Abstract method called")

	def getPrereq(self):
		raise Exception("Abstract method called")

	def getMem(self):
		raise Exception("Abstract method called")

	def getTime(self):
		raise Exception("Abstract method called")
	
	def getThreads(self):
		raise Exception("Abstract method called")

	@staticmethod
	def createAssembly(workspace, vital_parameters, assembly_type):
		if assembly_type=="assembly":
			return Assembly(workspace, vital_parameters)
		if assembly_type=="refineA":
			return RefineA(workspace, vital_parameters)

class Assembly(GenericAssembly):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters
		self.quality=None

		self.sd=0.2
		self.sf=0.2
		self.sr=0.03
		self.res=3.3
		self.color=1
		self.alignment_score_threshold=1
		self.max_rel_coverage_multiple=100
		self.max_rel_coverage_absolute=200
		self.max_rel_coverage_absolute_2=30
		self.bulge_coverage=20
		self.max_coverage=10
		self.min_coverage=10
		self.min_average_coverage=5
		self.min_maps=5
		self.min_contig_len=0.0
		self.end_trim=1
		self.chimera_pval=0.001
		self.chimera_num=3
		self.fast_bulge=1000
		self.fragile_preserve=False
		self.draftsize=1
		self.min_duplicate_len=1
		self.binary_output=True
		self.min_snr=2
		self.output_prefix="unrefined"
		self.add_alignment_filter=True
		self.alignment_filter_threshold=100
		self.alignment_filter_minlen_change=2.0
		self.alignment_filter_pval_change=0.5
		self.overwrite_output=True
		self.hide_branches=True
		self.send_output_to_file=True
		self.send_errors_to_file=True

		self.total_job_count=1

		self.autoGeneratePrereqs()

	def writeCode(self):
		code = "cd " + self.workspace.work_dir + "\n"
		code += "mkdir " + self.getStepDir() + "\n"
		code += "cd " + self.getStepDir() + "\n"
		code += "pwd\n"

		param_values=OrderedDict()
		param_values["-if"]= "../" + str(self.split_summary.getOutputFile())
		param_values["-af"]= "../" + str(self.pairwise_summary.getOutputFile())
		param_values["-XmapStatRead"]= "../" + str(self.molecule_stats.getOutputFile())
		param_values["-usecolor"]= str(self.color)
		param_values["-FP"]= str(self.vital_parameters.fp)
		param_values["-FN"]= str(self.vital_parameters.fn)
		param_values["-sd"]= str(self.sd)
		param_values["-sf"]= str(self.sf)
		param_values["-sr"]= str(self.sr)
		param_values["-res"]= str(self.res)
		param_values["-T"]= str(self.vital_parameters.pval)
		param_values["-S"]= str(self.alignment_score_threshold)
		param_values["-MaxRelCoverage"]= " ".join([str(self.max_rel_coverage_multiple), str(self.max_rel_coverage_absolute), str(self.max_rel_coverage_absolute_2)])
		param_values["-BulgeCoverage"]= str(self.bulge_coverage)
		param_values["-MaxCoverage"]= str(self.max_coverage)
		param_values["-MinCov"]= str(self.min_coverage)
		param_values["-MinAvCov"]= str(self.min_average_coverage)
		param_values["-MinMaps"]= str(self.min_maps)
		param_values["-MinContigLen"]= str(self.min_contig_len)
		param_values["-EndTrim"]= str(self.end_trim)
		param_values["-refine"]="0"
		param_values["-PVchim"]= " ".join([str(self.chimera_pval),str(self.chimera_num)])
		param_values["-FastBulge"]= str(self.fast_bulge)
		param_values["-FragilePreserve"]= str("1" if self.fragile_preserve else "0")
		param_values["-draftsize"]= str("1")
		param_values["-SideBranch"]= str(self.min_duplicate_len)
		param_values["-contigs_format"]= str("1" if self.binary_output else "0")
		param_values["-maxthreads"]= str(self.getThreads())
		maxmem=int(self.getMem()/self.getThreads())
		if maxmem<1:
			maxmem=1
		param_values["-maxmem"]= str(maxmem)
		param_values["-minlen"]= str(self.vital_parameters.min_molecule_len)
		param_values["-minsites"]= str(self.vital_parameters.min_molecule_sites)
		param_values["-minSNR"]= str(self.min_snr)
		param_values["-o"]= str(self.output_prefix)
		
		if self.add_alignment_filter:
			param_values["-AlignmentFilter"] = " ".join([str(self.alignment_filter_threshold), str(self.alignment_filter_minlen_change), str(self.alignment_filter_pval_change)])
		if self.overwrite_output:
			param_values["-force"] = ""
		if self.hide_branches:
			param_values["-SideChain"] = ""
		if self.send_output_to_file:
			param_values["-stdout"] = ""
		if self.send_errors_to_file:
			param_values["-stderr"] = ""

		param_list=[self.workspace.binaries["bng_assembler"]]
		for key in param_values:
			param_list.append(key)
			param_list.append(param_values[key])
		code += " ".join(param_list) + "\n"

		return [code]

	def getStepDir(self):
		return "_".join(["assembly", self.inpt.getStepDir(), "fp"+str(self.vital_parameters.fp), "fn"+str(self.vital_parameters.fn), "pval"+str(self.vital_parameters.pval), "minlen"+str(self.vital_parameters.min_molecule_len), "minsites"+str(self.vital_parameters.min_molecule_sites)])

	def autoGeneratePrereqs(self):
		self.inpt=Input(self.workspace)
		self.sort=Sort(self.workspace, copy(self.vital_parameters))
		self.molecule_stats=self.sort.getMoleculeStats()
		self.split=Split(self.workspace, copy(self.vital_parameters))
		self.split_summary=Summarize(self.workspace, self.split)
		self.pairwise_alignment=PairwiseAlignment(self.workspace, copy(self.vital_parameters))
		self.pairwise_summary=Summarize(self.workspace, self.pairwise_alignment)

	def getPrereq(self):
		return self.pairwise_summary

	def getMem(self):
		return self.workspace.resources.getLargeMemory()
	def getTime(self):
		return self.workspace.resources.getMediumTime()
	def getThreads(self):
		return 1

class RefineA(GenericAssembly):
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
		self.output_prefix="refineA"
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
		param_values["-LRbias"]=str(self.bias_for_low_likelihood_ratio)
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
		param_values["-o"]=self.output_prefix
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
		code+="  group_start=`echo $line | awk '{print $1}'`\n"
		code+="  group_end=`echo $line | awk '{print $NF}'`\n"
		code+="    " + " ".join(param_list) + "\n"
		code+="done < ../" + self.group_manifest.getOutputFile()

		return [code]
		
	def getStepDir(self):
		return "_".join(["refineA", self.inpt.getStepDir(), "fp"+str(self.vital_parameters.fp), "fn"+str(self.vital_parameters.fn), "pval"+str(self.vital_parameters.pval), "minlen"+str(self.vital_parameters.min_molecule_len), "minsites"+str(self.vital_parameters.min_molecule_sites)])

	def autoGeneratePrereqs(self):
		self.inpt=Input(self.workspace)
		self.sort=Sort(self.workspace, copy(self.vital_parameters))
		self.molecule_stats=self.sort.getMoleculeStats()
		self.split=Split(self.workspace, copy(self.vital_parameters))
		self.split_summary=Summarize(self.workspace, self.split)
		self.pairwise_alignment=PairwiseAlignment(self.workspace, copy(self.vital_parameters))
		self.pairwise_summary=Summarize(self.workspace, self.pairwise_alignment)
		self.assembly=Assembly(self.workspace, copy(self.vital_parameters))
		self.assembly_summary=Summarize(self.workspace, self.assembly)
		self.group_manifest=GroupManifest(self.workspace, self.assembly)

	def getPrereq(self):
		return self.group_manifest

	def getMem(self):
		return self.workspace.resources.getMediumMemory()
	def getTime(self):
		return self.workspace.resources.getLargeTime()
	def getThreads(self):
		return self.workspace.resources.getMediumThreads()

from Operations.BioNano.Assemble.Input import Input
from Operations.BioNano.Assemble.Sort import Sort
from Operations.BioNano.Assemble.Split import Split
from Operations.BioNano.Assemble.PairwiseAlignment import PairwiseAlignment
from Operations.BioNano.Assemble.Summarize import Summarize

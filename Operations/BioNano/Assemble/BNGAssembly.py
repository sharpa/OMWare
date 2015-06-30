# Module: Operations.BioNano.Assemble.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner and Assembler software to create an optical map de novo assembly
from Operations.Step import Step
from Operations.BioNano.Assemble.BNGSort import Sort
from Operations.BioNano.Assemble.BNGSplit import Split
from Operations.BioNano.Assemble.BNGPairwiseAlignment import PairwiseAlignment
from Operations.BioNano.Assemble.BNGSummarize import Summarize
from collections import OrderedDict

class Assembly(Step):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters

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

		self.autoGeneratePrereqs()

	def writeCode(self):
		code = "cd " + self.workspace.work_dir + "\n"
		code += "mkdir " + self.getStepDir() + "\n"
		code += "cd " + self.getStepDir() + "\n"
		code += "pwd\n"

		param_values=OrderedDict()
		param_values["-if"]= "../" + str(self.split.getListFile())
		param_values["-af"]= "../" + str(self.pairwise_alignment.getListFile())
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
		param_values["-refine"]= str(0)
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

		code += "result=`tail -n 1 ../" + self.getStepDir()  + "/" + self.output_prefix + ".stdout`\n"
		code += "if [[ \"$result\" != \"END of output\" ]]; then exit 1; else touch Complete.status; fi\n"

		return [code]

	def getStepDir(self):
		return "_".join(["assembly", self.workspace.input_file, "fp"+str(self.vital_parameters.fp), "fn"+str(self.vital_parameters.fn), "pval"+str(self.vital_parameters.pval), "minlen"+str(self.vital_parameters.min_molecule_len), "minsites"+str(self.vital_parameters.min_molecule_sites)])
	def getOutputFile(self):
		return self.getStepDir() + "/" + self.output_prefix + ".contigs"
	def getOutputFileExtension(self):
		return "contigs"

	def autoGeneratePrereqs(self):
		self.sort=Sort(self.workspace, self.vital_parameters)
		self.molecule_stats=self.sort.getMoleculeStats()
		self.split=Split(self.workspace, self.vital_parameters)
		self.pairwise_alignment=PairwiseAlignment(self.workspace, self.vital_parameters)

	def getPrereqs(self):
		return [Summarize(self.workspace, self.pairwise_alignment)]

	def getMem(self):
		return self.workspace.resources.getLargeMemory()
	def getTime(self):
		return self.workspace.resources.getMediumTime()
	def getThreads(self):
		return 1

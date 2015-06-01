# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner and Assembler software to create an optical map de novo assembly
from collections import OrderedDict
from Utils.MacbookProResources import MacbookProResources
from Assemble.BioNano.BNGSort import Sort
from Assemble.BioNano.BNGSplit import Split
from Assemble.BioNano.BNGPairwiseAlignment import PairwiseAlignment

class Assembly:
	def __init__(self, workspace, vital_parameters):
		# Workspace
		self.work_dir=workspace.work_dir
		self.input_file=workspace.input_file
		self.assembler_bin=workspace.binaries['bng_assembler']

		self.resources=MacbookProResources()

		# Parameters
		self.fp=vital_parameters.fp
		self.fn=vital_parameters.fn
		self.pval=vital_parameters.pval
		self.min_molecule_len=vital_parameters.min_molecule_len
		self.min_molecule_sites=vital_parameters.min_molecule_sites

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

	def writeCode(self):
		self.establishPrereqs()
		print("cd " + self.work_dir)
		print("mkdir " + self.getStepDir())
		print("cd " + self.getStepDir())
		param_values=OrderedDict()
		param_values["-if"]= str(self.split.getListFile())
		param_values["-af"]= str(self.pairwise_alignment.getListFile())
		param_values["-XmapStatRead"]= str(self.molecule_stats.getStatsFile())
		param_values["-usecolor"]= str(self.color)
		param_values["-FP"]= str(self.fp)
		param_values["-FN"]= str(self.fn)
		param_values["-sd"]= str(self.sd)
		param_values["-sf"]= str(self.sf)
		param_values["-sr"]= str(self.sr)
		param_values["-res"]= str(self.res)
		param_values["-T"]= str(self.pval)
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
		param_values["-maxthreads"]= str(self.resources.getMaxThreads())
		param_values["-maxmem"]= str(self.resources.getMaxMem())
		param_values["-minlen"]= str(self.min_molecule_len)
		param_values["-minsites"]= str(self.min_molecule_sites)
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

		param_list=[self.assembler_bin]
		for key in param_values:
			param_list.append(key)
			param_list.append(param_values[key])
		print(" ".join(param_list))

	def getStepDir(self):
		return self.work_dir + "/" + "_".join(["assembly", self.input_file, "fp"+str(self.fp), "fn"+str(self.fn), "pval"+str(self.pval), "minlen"+str(self.min_molecule_len), "minsites"+str(self.min_molecule_sites)])

	def establishPrereqs(self):
		self.sort=Sort(self.input_file)
		self.split=Split(self.input_file)
		self.pairwise_alignment=PairwiseAlignment(self.split)
		self.molecule_stats=self.sort.getMoleculeStats()
		self.prereqs=[self.sort, self.split, self.pairwise_alignment, self.molecule_stats]

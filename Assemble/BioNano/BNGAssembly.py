# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner and Assembler software to create an optical map de novo assembly
from Utils.MacbookProResources import MacbookProResources
from Assemble.BioNano.BNGSort import Sort
from Assemble.BioNano.BNGSplit import Split
from Assemble.BioNano.BNGPairwiseAlignment import PairwiseAlignment

class Assembly:
	def __init__(self):
		self.input_file="all.bnx"
		self.work_dir="/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_data_dir"
		self.assembler_bin="/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/Assembler"

		self.resources=MacbookProResources()

		self.color=1
		self.fp=1.5
		self.fn=.308
		self.sd=0.2
		self.sf=0.2
		self.sr=0.03
		self.res=3.3
		self.pval=1.11e-8
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
		self.min_molecule_len=100
		self.min_molecule_sites=6
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

		self.sort=Sort(self.input_file)
		self.split=Split(self.input_file)
		self.pairwise_alignment=PairwiseAlignment(self.split)
		self.molecule_stats=self.sort.getMoleculeStats()
		
		self.prereqs=[self.sort, self.split, self.pairwise_alignment, self.molecule_stats]
#		self.step_dir=""

	def writeCode(self):
		param_values={
			"-if": str(self.split.getListFile()),
			"-XmapStatRead": str(self.molecule_stats.getStatsFile()),
			"-usecolor": str(self.color),
			"-FP": str(self.fp),
			"-FN": str(self.fn),
			"-sd": str(self.sd),
			"-sf": str(self.sf),
			"-sr": str(self.sr),
			"-res": str(self.res),
			"-T": str(self.pval),
			"-S": str(self.alignment_score_threshold),
			"-MaxRelCoverage": " ".join([str(self.max_rel_coverage_multiple), str(self.max_rel_coverage_absolute), str(self.max_rel_coverage_absolute_2)]),
			"-BulgeCoverage": str(self.bulge_coverage),
			"-MaxCoverage": str(self.max_coverage),
			"-MinCov": str(self.min_coverage),
			"-MinAvCov": str(self.min_average_coverage),
			"-MinMaps": str(self.min_maps),
			"-MinContigLen": str(self.min_contig_len),
			"-EndTrim": str(self.end_trim),
			"-refine": str(0),
			"-PVchim": " ".join([str(self.chimera_pval),str(self.chimera_num)]),
			"-FastBulge": str(self.fast_bulge),
			"-FragilePreserve": str("1" if self.fragile_preserve else "0"),
			"-draftsize": str("1"),
			"-SideBranch": str(self.min_duplicate_len),
			"-contigs_format": str("1" if self.binary_output else "0"),
			"-maxthreads": str(self.resources.getMaxThreads()),
			"-maxmem": str(self.resources.getMaxMem()),
			"-minlen": str(self.min_molecule_len),
			"-minsites": str(self.min_molecule_sites),
			"-minSNR": str(self.min_snr),
			"-o": str(self.output_prefix),
		}
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


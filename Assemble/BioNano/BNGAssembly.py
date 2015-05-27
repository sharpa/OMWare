# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner and Assembler software to create an optical map de novo assembly
from Utils.MacbookProResources import MacbookProResources

class Assembly:
	def __init__(self):
		self.input="all.bnx"
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
		self.bulg_coverage=20
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

		self.sort=Sort(self.input)
		self.split=Split(self.sort)
		self.pairwise_alignment=PairwiseAlignment(self.split)
		self.molecule_stats=self.sort.getMoleculeStats()
		
		self.prereqs=[self.sort, self.split, self.pairwise_alignment, self.molecule_stats]
#		self.step_dir=""

	def writeCode(self):
		param_values={
			"-if": self.split.getListFile(),
			"-XmapStatRead": self.molecule_stats.getStatsFile(),
			"-usecolor": self.color,
			"-FP": self.fp,
			"-FN": self.fn,
			"-sd": self.sd,
			"-sf": self.sf,
			"-sr": self.sr,
			"-res": self.res,
			"-T": self.pval,
			"-S": self.alignment_score_threshold,
			"-MaxRelCoverage": " ".join(self.max_rel_coverage_multiple, self.max_rel_coverage_absolute, self.max_rel_coverage_absolute_2),
			"-BulgeCoverage": self.bulge_coverage,
			"-MaxCoverage": self.max_coverage,
			"-MinCov": self.min_coverage,
			"-MinAvCov": self.min_average_coverage,
			"-MinMaps": self.min_maps,
			"-MinContigLen": self.min_contig_len,
			"-EndTrim": self.end_trim,
			"-refine": 0,
			"-PVchim": " ".join(self.chimera_pval,self.chimera_num),
			"-FastBulge": self.fast_bulge,
			"-FragilePreserve": "1" if self.fragile_preserve else "0",
			"-draftsize": "1",
			"-SideBranch": self.min_duplicat_len,
			"-contigs_format": "1" if self.binary_output else "0",
			"-maxthreads": self.resources.getMaxThreads(),
			"-maxmem": self.resources.getMaxMem(),
			"-minlen": self.min_molecule_len,
			"-minsites": self.min_molecule_sites,
			"-minSNR": self.min_snr,
			"-o": self.output_prefix,
		}
		if self.add_alignment_filter:
			param_values["-AlignmentFilter"] = " ".join(self.alignment_filter_threshold, self.alignment_filter_minlen_change, self.alignment_filter_pval_change)
		if self.overwrite_output:
			param_values["-force"] = ""
		if self.hide_branches:
			param_values["-SideChain"] = ""
		if self.send_output_to_file:
			param_values["-stdout"] = ""
		if self.send_errors_to_file:
			param_values["-stderr"] = ""

		param_list=[assembler_bin]
		for key in param_values:
			param_list.append(key)
			param_list.append(param_values[key])
		print(" ".join(param_list))


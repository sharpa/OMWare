# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner to create a set of pairwise alignments
from Utils.MacbookProResources import MacbookProResources
from Assemble.BioNano.BNGSort import Sort
from Assemble.BioNano.BNGSplit import Split

class PairwiseAlignment:
	def __init__(self, input_file):
		self.input_file=input_file
		self.work_dir="/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_data_dir"
		self.ref_aligner_bin="/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/RefAligner"

		self.resources=MacbookProResources()

		self.color=1
		self.fp=1.5
		self.fn=.308
		self.sd=0.2
		self.sf=0.2
		self.sr=0.03
		self.res=3.3
		self.pval=1.11e-8
		self.min_alignment_sites=5
		self.min_alignment_score=1
		self.outlier_pval=0.0001
		self.endoutlier_pval=0
		self.repeat_max_shift=2
		self.repeat_pval_change=0.01
		self.repeat_pval_ratio=0.7
		self.repeat_min_change=0.6
		self.hash_window=5
		self.hash_min_sites=3
		self.hash_sd_max=2.2
		self.hash_sd_rms=1.2
		self.hash_relative_error=0.05
		self.hash_offset_kb=3.0
		self.hash_max_insert_errors=1
		self.hash_max_probe_errors=1
		self.hash_max_unresolved_sites=1
		self.target_resolution=1.2
		self.allow_no_splits=True
		self.allow_infinite_splits=False
		self.overwrite_output=True
		self.send_output_to_file=True
		self.send_error_to_file=True

		self.sort=Sort(self.input_file)
		self.split=Split(self.input_file)
		self.molecule_stats=self.sort.getMoleculeStats()
		prereqs=[self.sort, self.split, self.molecule_stats]

	def writeCode(self):
		param_values={
			"-usecolor": str(self.color),
			"-FP": str(self.fp),
			"-FN": str(self.fn),
			"-sd": str(self.sd),
			"-sf": str(self.sf),
			"-sr": str(self.sr),
			"-res": str(self.res),
			"-T": str(self.pval),
			"-maxmem": str(self.resources.getMaxMem()),
			"-A": str(self.min_alignment_sites),
			"-S": str(self.min_alignment_score),
			"-outlier": str(self.outlier_pval),
			"-endoutlier": str(self.endoutlier_pval),
			"-RepeatMask": " ".join([str(self.repeat_max_shift), str(self.repeat_pval_change)]),
			"-RepeatRec": " ".join([str(self.repeat_pval_ratio), str(self.repeat_min_change)]),
			"-hashgen": " ".join([str(self.hash_window), str(self.hash_min_sites), str(self.hash_sd_max), str(self.hash_sd_rms), str(self.hash_relative_error), str(self.hash_offset_kb), str(self.hash_max_insert_errors), str(self.hash_max_probe_errors), str(self.hash_max_unresolved_sites)]),
			"-hash": "",
			"-mres": str(self.target_resolution),
			"-nosplit": "2" if self.allow_no_splits else "0" if self.allow_infinite_splits else "1",
			"-maxthreads": str(self.resources.getMaxThreads()),
			"-XmapStatRead": str(self.molecule_stats.getStatsFile())
		}
		if self.overwrite_output:
			param_values["-f"]=""
#		if not self.generate_hash: # Order matters...
#			param_values["-hash"]
		if self.send_output_to_file:
			param_values["-stdout"]=""
		if self.send_error_to_file:
			param_values["-stderr"]=""
		
		totalBlocks=self.split.getBlockCount()
		totalJobs=totalBlocks*(totalBlocks+1)/2 
		currentJob = 0
		for i in range(1,totalBlocks+1):
			file1=self.split.getBlock(i)
			for j in range(i,totalBlocks + 1):
				file2=self.split.getBlock(j)

				param_values["-i"]=file1
				if i==j :
					if "-first" in param_values:
						del param_values["-first"]
					if "-1" in param_values:
						del param_values["-1"]
					if "-i " in param_values:
						del param_values["-i "]
				else :
					param_values["-first"]=""
					param_values["-1"]=""
					param_values["-i "]=file2

				param_values["-o"]='pairwise%dof%d' % (currentJob+1, totalJobs)

				param_list=[self.ref_aligner_bin]
				for key in param_values:
					param_list.append(key)
					param_list.append(param_values[key])
				print(" ".join(param_list))

				currentJob += 1

	def getListFile(self):
		return "align.list"

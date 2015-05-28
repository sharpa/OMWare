# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner and Assembler software to create sort an input dataset
from Utils.MacbookProResources import MacbookProResources
from Assemble.BioNano.BNGMoleculeStats import MoleculeStats

class Sort:
	def __init__(self, input_file):
		self.input_file=input_file
		self.ref_aligner_bin="/Users/sharap/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/RefAligner"

		self.resources=MacbookProResources()

		self.output_prefix="all_sorted"
		self.min_molecule_len=100
		self.min_molecule_sites=6
		self.min_snr=2
		self.overwrite_output=True
		self.send_output_to_file=True
		self.send_errors_to_file=True

		self.molecule_stats=self.getMoleculeStats()
		self.prereqs=[]

	def writeCode(self):
		param_values={
			"-i": self.input_file,
			"-maxthreads": str(self.resources.getMaxThreads()),
			"-merge": "",
			"-sort-idinc": "",
			"-bnx": "",
			"-o": self.output_prefix,
			"-minlen": str(self.min_molecule_len),
			"-minsites": str(self.min_molecule_sites),
			"-minSNR": str(self.min_snr),
			"-XmapStatWrite": self.molecule_stats.getStatsFile()
		}
		if self.overwrite_output:
			param_values["-f"] = ""
		if self.send_output_to_file:
			param_values["-stdout"] = ""
		if self.send_errors_to_file:
			param_values["-stderr"] = ""
		
		param_list=[self.ref_aligner_bin]
		for key in param_values:
			param_list.append(key)
			param_list.append(param_values[key])
		print(" ".join(param_list))

	def getMoleculeStats(self):
		return MoleculeStats(self.input_file)
	def getSortedFile(self):
		return self.output_prefix + ".bnx"

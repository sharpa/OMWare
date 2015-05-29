#!/usr/bin/python

# The purpose of this test is to run several assemblies
#	to assess the effect of different coverage level
#	by randomly removing molecules


work_dir="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir"
input_file="all_abridged.bnx"
assembler_bin="/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/Assembler"

class dummySort:
	def __init__(self):
		pass
	def getMoleculeStats(self):
		return dummyMoleculeStats()

class dummyMoleculeStats:
	def __init__(self):
		pass
	def getStatsFile(self):
		return "/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir/molecule_stats.txt"

class dummySplit:
	def __init__(self, input_file):
		self.input_file=input_file
	def getListFile(self):
		return "/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir/"+self.input_file

class dummyPairwise:
	def __init__(self):
		pass
	def getListFile(self):
		return "/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir/pairwise/align.list"

from Assemble.BioNano.BNGAssembly import Assembly
from Utils.CD import CD
with CD(work_dir):
	for cutoff in xrange(9,0,-1):
		assembly=Assembly()
		assembly.input_file=input_file+"_" + str(cutoff*10)
		assembly.work_dir=work_dir
		assembly.assembler_bin=assembler_bin

		assembly.fp=1.5
		assembly.fn=.386
		assembly.pval=1.11e-6
		assembly.output_prefix="unrefined_" + str(cutoff*10)

		assembly.sort=dummySort()
		assembly.split=dummySplit(assembly.input_file)
		assembly.pairwise_alignment=dummyPairwise()
		assembly.molecule_stats=dummyMoleculeStats()

		assembly.writeCode()

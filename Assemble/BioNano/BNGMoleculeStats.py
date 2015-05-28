# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# The purpose of this module is to perform a file name conversion from 
# a given input file to the associated molecule stats file

class MoleculeStats:
	def __init__(self, input_file):
		self.input_file=input_file
	def getStatsFile(self):
		return "molecule_stats.txt"

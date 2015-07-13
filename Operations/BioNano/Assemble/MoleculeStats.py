# Module: Operations.BioNano.Assemble.MoleculeStats
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# The purpose of this module is to perform a file name conversion from 
# a given input file to the associated molecule stats file

class MoleculeStats:
	def __init__(self, step_dir):
		self.step_dir=step_dir
	def __eq__(self, other):
		if other is None:
			return False
		if self.__class__ != other.__class__:
			return False
		return self.step_dir==other.step_dir
	def __ne__(self, other):
		return not self == other
	def getOutputFile(self):
		return self.step_dir+"/molecule_stats.txt"

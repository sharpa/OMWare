# Module: Operations.BioNano.Assemble.VitalParameters
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/01/2015
# 
# The purpose of this module is to encapsulate and provide services for vital assembly parameters

class VitalParameters:
	def __init__(self, fp, fn, pval, min_molecule_len, min_molecule_sites):
		self.fp=fp
		self.fn=fn
		self.pval=pval
		self.min_molecule_len=min_molecule_len
		self.min_molecule_sites=min_molecule_sites
		self.blocks=None
	def __eq__(self, other):
		if other is None:
			return False
		if self.__class__!=other.__class__:
			return False
		return self.__dict__==other.__dict__
	def __ne__(self, other):
		return not self == other

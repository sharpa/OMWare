# Module: Operations.Subset.Subsetter
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/05/2015
# 
# The purpose of this module remove molecules from (or keep them in)
# an input .bnx file based on their attributes
from POMMIO import POMMIO

class Subsetter(object):
	def __init__(self, input_file, output_file):
		self.input_file=input_file
		self.output_file=output_file

	def subset(self, criteria, output_file=None):
		if output_file==None:
			output_file=self.output_file

		with open(output_file, "w") as o_file:
			pommio=POMMIO(self.input_file)
			for header in pommio.getHeaders():
				o_file.write(header)
			for molecule in pommio.parse("bnx"):
				if criteria(molecule):
					pommio.write(molecule, o_file, "bnx")

	def keep_greater(self, attribute, limit):
		if attribute=="length":
			def criteria(molecule):
				return molecule.length>limit
		# TODO many more to implement...
		self.subset(criteria)

	def remove_equals(self, attribute, values):
		if attribute=="run_id":
			def criteria(molecule):
				if molecule.run_id in values:
					return False
				return True
		# TODO many more to implement...
		self.subset(criteria)

# Module: Operations.Subset.Subsetter
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/05/2015
# 
# The purpose of this module remove molecules from (or keep them in)
# an input .bnx file based on their attributes
from Operations.BioNano.files import BnxFile

class Subsetter(object):
	def __init__(self, input_file, output_file):
		self.input_file=input_file
		self.output_file=output_file

	def subset(self, criteria, output_file=None):
		if output_file==None:
			output_file=self.output_file

		with open(output_file, "w") as o_file:
			bnx_file=BnxFile(self.input_file)
			for header in bnx_file.getHeaders():
				o_file.write(header)
			for molecule in bnx_file.parse():
				if criteria(molecule):
					bnx_file.write(molecule, o_file)

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

class RunCharacterizer(object):
	def __init__(self, input_file):
		self.input_file=input_file
		self.dataset_stats={}

	def __str__(self):
		output=""
		for key in self.dataset_stats.keys():
			output+=str(key) + "	" + str(self.dataset_stats[key]["density"]) + "\n"
		return output

	def characterize(self):
		bnx_file=BnxFile(self.input_file)
		for molecule in bnx_file.parse():
			run_id=molecule.run_id
			if run_id not in self.dataset_stats:
				self.dataset_stats[run_id]={"length": 0.0, "labels": 0.0}
			self.dataset_stats[run_id]["length"] += float(molecule.length)
			self.dataset_stats[run_id]["labels"] += float(molecule.num_labels)
		for run_id in self.dataset_stats:
			stats=self.dataset_stats[run_id]
			stats["density"] = stats["labels"] / (stats["length"] / (1000 * 100))



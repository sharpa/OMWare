# Module: POMMIO
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to import and export optical maps
# from/into a variety of file formats

class POMMIO:
	def __init__(self, input_file):
		self.input_file=input_file

	def getHeaders(self):
		headers=[]
		with open(self.input_file, "r") as i_file:
			for line in i_file:
				if line[0]=="#":
					headers.append(line)
				else:
					break
		return headers

	def parse(self, format):
		result=[]
		for i, length in enumerate(xrange(1,100,5)):
			new_mol=Molecule(i, length)
			result.append(new_mol)
		return result
	def write(self, molecule, o_file, format):
		o_file.write("	".join(["0", str(molecule.id), str(molecule.length)]) + "\n")

class Molecule:
	def __init__(self, id, length):
		self.id=id
		self.length=length

	def shrink(self, distance):
		self.length=distance

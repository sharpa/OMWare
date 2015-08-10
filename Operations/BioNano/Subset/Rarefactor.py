# Module: Utils
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/28/2015
# 
# The purpose of this module is to take an input dataset
# and return a new dataset that has a random subset of the input
# by random removal of whole or partial molecules
import random
from Operations.BioNano.files import BnxFile

class Rarefactor:
	def __init__(self, input_file):
		self.input_file=input_file

	def generateReducedDataset(self, proportion, output_file=None):
		if proportion > 1 or proportion < 0:
			raise Exception("proportion must be between 1 and 0")
		
		if output_file is None:
			output_file=self.input_file + "_" + str(int(proportion*100))

		with open(output_file, "w") as o_file:
			bnx_file=BnxFile(self.input_file)
			headers=bnx_file.getHeaders()
			for header in headers:
				o_file.write(header)
			o_file.write("# Reduced to " + str(proportion*100) + "% of the original\n")

			total_length=0.0
			molecule_lengths={}
			molecule_ids=[]
			for molecule in bnx_file.parse():
				total_length+=molecule.length
				molecule_lengths[molecule.id] = molecule.length
				molecule_ids.append(molecule.id)
			
			seed=random.random()
			random.seed(seed)
			o_file.write("# Random seed for reduction: " + str(seed) + "\n")

			target_removed_length=total_length*(1.0-proportion)
			removed_length=0
			total_molecules=len(molecule_ids)
			removed=set()
			abridged={}
			while removed_length < target_removed_length:
				list_index=int(random.random()*total_molecules)
				candidate=molecule_ids[list_index]
				removed_length+=molecule_lengths[candidate]

				del[molecule_ids[list_index]]
				total_molecules-=1
				
				if removed_length <= target_removed_length:
					removed.add(candidate)
				else:
					excess_distance=removed_length-target_removed_length
					abridged[candidate]=excess_distance

			for molecule in bnx_file.parse():
				if molecule.id in removed:
					continue
				if molecule.id in abridged:
					molecule.shrink(abridged[molecule.id])
				bnx_file.write(molecule, o_file)




# Module: Operations.BioNano.Assemble.GroupManifest
# Version: 0.1
# Author: Aaron Sharp
# Date: 07/08/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner and Assembler software to create an optical map de novo assembly
from Operations.Step import Step
import os
import re 

class GroupManifest(Step):
	def __init__(self, workspace, assembly):
		self.workspace=workspace
		self.assembly=assembly
		self.quality=None

	def writeCode(self):
		code="cd " + self.workspace.work_dir + "\n"
		code+="mkdir " + self.getStepDir() + "\n"
		code+="cd " + self.getStepDir() + "\n"
		code+="pwd\n"
		code+="python -c 'from Utils.Workspace import Workspace;"
		code+="from Operations.BioNano.Assemble.VitalParameters import VitalParameters;"
		code+="from Operations.BioNano.Assemble.Assembly import Assembly;"
		code+="from Operations.BioNano.Assemble.GroupManifest import GroupManifest;"
		code+="ws=Workspace(\"" + self.workspace.work_dir + "\", \"" + self.workspace.input_file + "\");"
		code+="vp=VitalParameters(" + str(self.assembly.vital_parameters.fp) + ", " + str(self.assembly.vital_parameters.fn) + ", " + str(self.assembly.vital_parameters.pval) + ", " + str(self.assembly.vital_parameters.min_molecule_len) + ", " + str(self.assembly.vital_parameters.min_molecule_sites) + ");"
		code+="gm=GroupManifest(ws, Assembly(ws, vp));"
		code+="gm.makeGroupManifestFile()'"
		return [code]
		
	def makeGroupManifestFile(self):
		with open("../" + self.getOutputFile(), "w") as manifest_file:
			try:
				with open("weight_stats.txt") as weight_file:
					self._makeGroupManifestFile(weight_file, manifest_file)
			except IOError:
				self.makeWeightStatsFile()
				with open("weight_stats.txt") as weight_file:
					self._makeGroupManifestFile(weight_file, manifest_file)
		with open("Complete.status", "w"):
			pass
	
	def _makeGroupManifestFile(self, weight_file, manifest_file):
		total_weight=0
		num_contigs=0
		contigs=[]
		weights={}
		for line in weight_file:
			num_contigs+=1
			info=line.split()
			length=float(info[1])
			sites=int(info[2])

			weight=sites*sites*sites / (length*length)
			total_weight+=weight
			weights[info[0]] = weight
			contigs.append(info[0])

		manifest_file.write("# Manifest file for " + self.assembly.output_prefix + "\n")

		bunch_num=12
		if num_contigs < 3600:
			bunch_num=num_contigs/300
		elif num_contigs > 12000:
			bunch_num=num_contigs/1000
		if bunch_num < 1:
			bunch_num=1

		weight_limit=bunch_num * (total_weight/num_contigs)

		current_groups=""
		current_group_weight=0
		current_group_count=0
		for contig in contigs:
			contig_id=re.sub(".cmap", "", re.sub("unrefined_contig", "", contig))

			current_group_count+=1
			current_group_weight+=weights[contig]

			if (current_group_count<=bunch_num and current_group_weight<=weight_limit):
				if current_groups == "":
					current_groups=str(contig_id)
				else:
					current_groups=current_groups + " " + str(contig_id)
			else:
				if current_groups != "":
					manifest_file.write(str(current_groups) + "\n")
				current_groups=str(contig_id)
				current_group_weight=weights[contig]
				current_group_count=1
		manifest_file.write(str(current_groups) + "\n")
		
	def makeWeightStatsFile(self):
		with open("weight_stats.txt", "w") as weight_file:
			CONTIG_FILE=re.compile(self.assembly.output_prefix + "_contig[\d]+\.cmap")
			files=os.listdir("../" + self.assembly.getStepDir())
			for a_file in files:
				if CONTIG_FILE.match(a_file) is None:
					continue
				with open("../" + self.assembly.getStepDir() + "/" + a_file) as contig_file:
					for line in contig_file:
						if line[0]=="#":
							continue
						line_data=line.split()
						weight_file.write(" ".join(line_data[0:3]) + "\n")
						break
			
		
	def getStepDir(self):
		return "manifest_for_" + self.assembly.getStepDir()
	def getOutputFile(self):
		return self.getStepDir() + "/" + self.assembly.output_prefix+".group_manifest"
	def getOutputFileExtension(self):
		return "group_manifest"
	def autoGeneratePrereqs(self):
		pass
	def getPrereqs(self):
		return [self.assembly]

	def getMem(self):
		return self.workspace.resources.getSmallMemory()
	def getTime(self):
		return self.workspace.resources.getSmallTime()
	def getThreads(self):
		return 1

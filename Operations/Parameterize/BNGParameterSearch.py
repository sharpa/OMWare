# Module: Parameterize.BNGParameterSearch
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/11/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run many assemblies at a variety of input parameters to determine 
# which set is most appropriate to the data
from Operations.Step import Step
from Operations.Assemble.BioNano.BNGVitalParameters import VitalParameters
from Operations.Assemble.BioNano.BNGAssembly import Assembly
from Operations.Assemble.BioNano.BNGPairwiseAlignment import PairwiseAlignment
from Operations.SBATCHCodeFormatter import CodeFormatter

class ParameterSearch(Step):
	def __init__(self, workspace, genome_size_mb):
		self.workspace=workspace

		recommended_pval=1e-5/float(genome_size_mb)
		self.pvals=[recommended_pval/10000, recommended_pval/100, recommended_pval, recommended_pval*100, recommended_pval*10000]
		self.falsehoods=[ [.5, .150],
				[.5, .300],
				[.5, .450],
				[1.5, .150],
				[1.5, .300],
				[1.5, .450],
				[2.5, .150],
				[2.5, .300],
				[2.5, .450] ]
		self.minlens=[100, 150, 180]
		self.minsites=[6, 8, 10]

		self.assemblies=set()
		self.pairwise_alignments=set()
		self.splits=set()
		self.sorts=set()

		self.code_formatter=CodeFormatter()
		

	def writeCode(self):
		for falsehood in self.falsehoods:
			for pval in self.pvals:
				for minlen in self.minlens:
					for minsite in self.minsites:
						self.createDumbAssembly(falsehood, pval, minlen, minsite)
		new_sorts=set() ###
		new_splits=set() ###
		new_pas=set() ###
		for assembly in self.assemblies:
			self.educateAssembly(assembly)			
			new_sorts.add(assembly.sort)
			new_splits.add(assembly.split)
			new_pas.add(assembly.pairwise_alignment)
			
		print("sorts")
		for x in new_sorts:
			print(x)
		print("splits")
		for x in new_splits:
			print(x)
		print("pairwise_alignments")
		for x in new_pas:
			print(x)
		print("assemblies")
		for x in self.assemblies:
			print(x)

#		step_parts=self.code_formatter.formatCode(assembly) ###
		### modify steps ###
#		self.code_formatter.serializeCode(step_parts) ###
						

	# A dumb assembly uses it's own default prereqs, instead of someone else's
	def createDumbAssembly(self, falsehood, pval, minlen, minsite):
		vital_params=VitalParameters(falsehood[0], falsehood[1], pval, minlen, minsite)
		assembly=Assembly(self.workspace, vital_params)
		self.assemblies.add(assembly)
		self.pairwise_alignments.add(assembly.pairwise_alignment)
		self.splits.add(assembly.split)
		self.sorts.add(assembly.sort)

	def educateAssembly(self, assembly):
		lowest_sort=None
		for sort in self.sorts:
			if not self.isCompatible(sort, assembly):
				continue
			if self.isLower(sort, lowest_sort):
				lowest_sort=sort
		assembly.sort=lowest_sort
		assembly.molecule_stats=lowest_sort.getMoleculeStats()

		lowest_split=None
		for split in self.splits:
			if not self.isCompatible(split, assembly):
				continue
			if self.isLower(split, lowest_split):
				lowest_split=split
		lowest_split.sort=lowest_sort
		lowest_split.molecule_stats=lowest_sort.getMoleculeStats()
		assembly.split=lowest_split

		lowest_pairwise_alignment=None
		for pairwise_alignment in self.pairwise_alignments:
			if not self.isCompatible(pairwise_alignment, assembly):
				continue
			if self.isLower(pairwise_alignment, lowest_pairwise_alignment):
				lowest_pairwise_alignment=pairwise_alignment
		lowest_pairwise_alignment.split=lowest_split
		lowest_pairwise_alignment.sort=lowest_sort
		lowest_pairwise_alignment.molecule_stats=lowest_sort.getMoleculeStats()
		assembly.pairwise_alignment=lowest_pairwise_alignment

	def isCompatible(self, candidate, voter):
		if isinstance(candidate, PairwiseAlignment):
			return self.isCompatiblePairwiseAlignment(candidate, voter)

		isCompatible=True
		if candidate.vital_parameters.min_molecule_len>voter.vital_parameters.min_molecule_len:
			isCompatible=False
		if candidate.vital_parameters.min_molecule_sites>voter.vital_parameters.min_molecule_sites:
			isCompatible=False

		return isCompatible

	def isCompatiblePairwiseAlignment(self, candidate, voter):
		isCompatible=True
		if candidate.vital_parameters.fp!=voter.vital_parameters.fp:
			isCompatible=False
		if candidate.vital_parameters.fn!=voter.vital_parameters.fn:
			isCompatible=False
		if candidate.vital_parameters.pval<voter.vital_parameters.pval:
			isCompatible=False
		return isCompatible

	def isLower(self, contender, champion):
		if champion is None:
			return True
		isLower=True
		if contender.vital_parameters.min_molecule_len > champion.vital_parameters.min_molecule_len:
			isLower=False
		if contender.vital_parameters.min_molecule_sites > champion.vital_parameters.min_molecule_sites:
			isLower=False
		if contender.vital_parameters.pval < champion.vital_parameters.pval:
			isLower=False
		return isLower

	def getStepDir(self):
		return self.workspace.work_dir

	def getOutputFileExtension(self):
		return ""

	def autoGeneratePrereqs(self):
		# Generate a list
		pass

	def getPrereqs(self):
		return []

	def isComplete(self):
		# Check isComplete on list members
		return False

	def getMem(self):
		return self.workspace.resources.getSmallMemory()
	def getTime(self):
		return self.workspace.resources.getSmallTime()
	def getThreads(self):
		return 1

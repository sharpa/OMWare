# Module: Parameterize.ParameterSearch
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/11/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run many assemblies at a variety of input parameters to determine 
# which set is most appropriate to the data
from collections import OrderedDict
from Operations.Step import Step
from Operations.Step import Quality
from Operations.BioNano.Assemble.VitalParameters import VitalParameters
from Operations.BioNano.Assemble.Assembly import Assembly
from Operations.BioNano.Assemble.PairwiseAlignment import PairwiseAlignment
from Operations.BioNano.Assemble.Summarize import Summarize

class ParameterSearch(Step):
	def __init__(self, workspace, genome_size_mb):
		self.workspace=workspace
		self.quality=None

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

		self.input_file_blocks=None

		self.sorts=set()
		self.splits=set()
		self.pairwise_alignments=set()
		self.assemblies=set()
		self.autoGeneratePrereqs()
		
	def optimizeFalsehoods(self, avg_label_density, expected_label_density):
		new_falsehoods=[]

		fp=0.0
		while fp <= 3.0:
			true_label_density=avg_label_density-fp
			fn=1.00 - (true_label_density/expected_label_density)
			
			new_falsehoods.append([fp, fn])

			fp+=0.5

		self.falsehoods=new_falsehoods

	def writeCode(self):
                run_assemblies=set()
                for assembly in self.assemblies:
                        if not assembly.isComplete():
                                run_assemblies.add(assembly)

                necessary_sorts=set()
                necessary_splits=set()
                necessary_pas=set()
                for assembly in run_assemblies:
                        self.educateAssembly(assembly)
                        necessary_sorts.add(assembly.sort)
                        necessary_splits.add(assembly.split)
                        necessary_pas.add(assembly.pairwise_alignment)

                run_sorts=set()
                for sort in necessary_sorts:
                        if not sort.isComplete():
                                run_sorts.add(sort)

                run_splits=set()
                split_summaries=set()
                for split in necessary_splits:
                        if not split.isComplete():
                                run_splits.add(split)
                                split_summaries.add(Summarize(self.workspace, split))

                run_pas=set()
                pairwise_summaries=set()
                for pairwise in necessary_pas:
                        if not pairwise.isComplete():
                                run_pas.add(pairwise)
                                pairwise_summaries.add(Summarize(self.workspace, pairwise))

                return [run_sorts, run_splits, split_summaries, run_pas, pairwise_summaries, run_assemblies]

	# A dumb assembly uses it's own default prereqs, instead of someone else's
	def createDumbAssembly(self, falsehood, pval, minlen, minsite):
		vital_params=VitalParameters(falsehood[0], falsehood[1], pval, minlen, minsite)
		vital_params.blocks=self.input_file_blocks

		assembly=Assembly(self.workspace, vital_params)
		self.assemblies.add(assembly)
		self.pairwise_alignments.add(assembly.pairwise_alignment)
		self.splits.add(assembly.split)
		self.sorts.add(assembly.sort)

		if self.input_file_blocks is None:
			self.input_file_blocks=assembly.split.total_job_count

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
		assembly.split_summary=Summarize(assembly.workspace, assembly.split)

		lowest_pairwise_alignment=None
		for pairwise_alignment in self.pairwise_alignments:
			if not self.isCompatible(pairwise_alignment, assembly):
				continue
			if self.isLower(pairwise_alignment, lowest_pairwise_alignment):
				lowest_pairwise_alignment=pairwise_alignment
		lowest_pairwise_alignment.split=lowest_split
		lowest_pairwise_alignment.split_summary=Summarize(lowest_pairwise_alignment.workspace, lowest_split)
		lowest_pairwise_alignment.sort=lowest_sort
		lowest_pairwise_alignment.molecule_stats=lowest_sort.getMoleculeStats()
		assembly.pairwise_alignment=lowest_pairwise_alignment
		assembly.pairwise_summary=Summarize(assembly.workspace, assembly.pairwise_alignment)

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
		self.assemblies=set()
		for falsehood in self.falsehoods:
                        for pval in self.pvals:
                                for minlen in self.minlens:
                                        for minsite in self.minsites:
                                                self.createDumbAssembly(falsehood, pval, minlen, minsite)

	def getPrereqs(self):
		return []

	def isComplete(self):
		for assembly in self.assemblies:
			if not assembly.isComplete():
				return False
		return True 

	def loadQualityReportItems(self):
		report=OrderedDict()
		report["Assembly Directory\tContig Count\tLength in Basepairs"]=1
		if self.quality is None:
			self.createQualityObject()
		for assembly in self.quality.assemblies:
			main_stats=[assembly]
			main_stats.extend(self.quality.assemblies[assembly][5:7])
			report["\t".join(main_stats)]=1
			other_stats=[""]
			other_stats.extend(self.quality.assemblies[assembly])
			report["\t".join(other_stats)]=2
		return report
		
	def createQualityObject(self):
##		if not self.isComplete():
##			raise Exception("Cannont ascertain quality if this step is not complete")
		self.quality=Quality(assemblies={})
		for assembly in self.assemblies:
			if not assembly.isComplete():
				continue
			count=assembly.getQuality_count()
			length=assembly.getQuality_length()
			self.quality.assemblies[assembly.getStepDir()]=[str(assembly.vital_parameters.fp), str(assembly.vital_parameters.fn), str(assembly.vital_parameters.pval), str(assembly.vital_parameters.min_molecule_len), str(assembly.vital_parameters.min_molecule_sites), str(count), str(length)]
		self.saveQualityObjectToFile()
	def getMem(self):
		return self.workspace.resources.getSmallMemory()
	def getTime(self):
		return self.workspace.resources.getSmallTime()
	def getThreads(self):
		return 1

# Module: Operations.BioNano.Compare.ReferenceAlign
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/28/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run compare a BNG assembly to an in silico digested reference map
from Operations.Step import Step
from sys import maxint

class ReferenceAlignment(Step):
	def __init__(self, workspace, merge, ref_file):
		self.workspace=workspace
		self.merge=merge
		self.ref_file=ref_file
		self.quality=None

		file_data=self.ref_file.split('/')
		prefix_data=file_data[len(file_data)-1].split('.')

		self.output_prefix=prefix_data[0]
		self.send_output_to_file=True
		self.send_error_to_file=True
		self.output_veto_regex="_intervals.txt$"
		self.res=2.9
		self.pval=1e-10 ###
		self.fp=0.6 ###
		self.fn=0.06 ###
		self.sf=0.20
		self.sd=0.10
#		self.sd=0.20
#		self.sr=0.03
		self.allow_overhang=True
		self.outlier_pval=0.0001
		self.end_outlier_pval=0.001
		self.max_query_alignment_interval=12
		self.max_reference_alignment_interval=12
		self.min_sites_for_chimera=14
		self.hash_window=5
		self.hash_min_sites=3
		self.hash_sd_max=2.2
		self.hash_sd_rms=1.2
		self.hash_relative_error=0.05
		self.hash_offset_kb=3.0
		self.hash_max_insert_errors=1
		self.hash_max_probe_errors=1
		self.hash_max_unresolved_sites=1
		self.hash_delta=50
		self.target_resolution=1e-3
		self.resolution_reduction=1.2
		self.allow_no_splits=True
		self.allow_infinite_splits=False
		self.scale_bias_wt=0
		self.overwrite_output=True
		self.print_indel_file=True

		self.autoGeneratePrereqs()

	def __hash__(self):
		return hash((self.workspace.input_file, self.workspace.work_dir, self.ref_file))

	def __str__(self):
		return("Comparison of " + self.workspace.input_file + " to " + self.ref_file)

	def writeCode(self):
		code="cd " + self.workspace.work_dir + "\n"
		code+="mkdir " + self.getStepDir() + "\n"
		code+="cd " + self.getStepDir() + "\n"
		code+="pwd" + "\n"

		param_values=OrderedDict()
		param_values["-ref"]=  "../" + self.anchor.getOutputFile()
		param_values["-i"]=  "../" + self.query.getOutputFile()
		param_values["-o"]=  self.output_prefix
		param_values["-maxthreads"]=  str(self.getThreads())
		param_values["-insertThreads"]=  str(self.getThreads())
		maxmem=self.getMem() / self.getThreads()
		if maxmem < 1:
			maxmem=1
		param_values["-maxmem"]=  str(maxmem)
		param_values["-output-veto-filter"]=  self.output_veto_regex
		param_values["-res"]=  str(self.res)
		param_values["-T"]=  str(self.pval)
		param_values["-FP"]=  str(self.fp)
		param_values["-FN"]=  str(self.fn)
		param_values["-sf"]=  str(self.sf)
		param_values["-sd"]=  str(self.sd)
		param_values["-extend"]=  "1" if self.allow_overhang else "0"
		param_values["-outlier"]=  str(self.outlier_pval)
		param_values["-endoutlier"]=  str(self.end_outlier_pval)
		param_values["-deltaX"]=  str(self.max_query_alignment_interval)
		param_values["-deltaY"]=  str(self.max_reference_alignment_interval)
		param_values["-xmapchim"]=  str(self.min_sites_for_chimera)
		param_values["-hashgen"]=  " ".join([str(self.hash_window), str(self.hash_min_sites), str(self.hash_sd_max), str(self.hash_sd_rms), str(self.hash_relative_error), str(self.hash_offset_kb), str(self.hash_max_insert_errors), str(self.hash_max_probe_errors), str(self.hash_max_unresolved_sites)])
		param_values["-hash"]=  ""
		param_values["-hashdelta"]=  str(self.hash_delta)
		param_values["-mres"]=  str(self.target_resolution)
		param_values["-rres"]=  str(self.resolution_reduction)
		param_values["-nosplit"]=  "2" if self.allow_no_splits else "0" if self.allow_infinite_splits else "1"
		param_values["-biaswt"]=  str(self.scale_bias_wt)

		if self.send_output_to_file:
			param_values["-stdout"]=""
		if self.send_error_to_file:
			param_values["-stderr"]=""
		if self.overwrite_output:
			param_values["-force"]=""
		if self.print_indel_file:
			param_values["-indel"]=""

		param_list=[self.workspace.binaries["bng_ref_aligner"]]
		for key in param_values:
			param_list.append(key)
			param_list.append(param_values[key])
		code+=" ".join(param_list)
		return [code]

	def getStepDir(self):
		return "_".join(["comparison", self.workspace.input_file, self.ref_file])

	def getOutputFile(self):
		return self.getStepDir() + "/" + self.output_prefix + "." + self.getOutputFileExtension()

	def getOutputFileExtension(self):
		return "xmap"

	def autoGeneratePrereqs(self):
		work_dir=self.workspace.work_dir
		self.anchor=Input(Workspace(work_dir, self.ref_file))
		self.query=Input(Workspace(work_dir, self.merge.getOutputFile()))

	def getPrereq(self):
		return self.merge

	def loadQualityReportItems(self):
		if self.quality is None:
			self.loadQualityObjectFromFile()

		report_items=OrderedDict()
		report_items["Num alignments: " + str(self.quality.num_alignments)]=1
		report_items["Total length: " + str(self.quality.total_length)]=2
		report_items["Query length: " + str(self.quality.query_length)]=3
		report_items["Proportion of query with match: "  + str(self.quality.proportion_query)]=1
		report_items["Anchor length: " + str(self.quality.anchor_length)]=3
		report_items["Proportion of anchor with match: " + str(self.quality.proportion_anchor)]=1

		report_items["Total confidence: " + str(self.quality.total_confidence)]=2
		report_items["Max confidence: " + str(self.quality.max_confidence)]=2
		report_itmes["Min confidence: " + str(self.quality.min_confidence)]=2
		report_items["Average confidence: " + str(self.quality.average_confidence)]=3
		report_items["Weighted average confidence: " + str(self.quality.weighted_average_confidence)]=1
		return report_items

	def createQualityObject(self):
		query_length=0.0
		anchor_length=0.0
		num_alignments=0
		confidences=[]
		total_confidence=0.0
		total_length=0.0
		max_confidence=0.0
		min_confidence=maxint
		
		for alignment in XmapFile(self.getOutputFile()).parse():
			num_alignments+=1

			conf=alignment.confidence 
			total_confidence+=conf

			if conf > max_confidence:
				max_confidence=conf
			if conf < min_confidence:
				min_confidence=conf

			length=max(alignment.query_len, alignment.anchor_len)
			total_length+=length

			confidences.append(conf, length)

		weighted_average_confidence=0.0
		for conf, length in confidences:
			adjustment=length / total_length
			adjusted_confidence=conf * adjustment
			weighted_average_confidence+=adjusted_confidence

		proportion_query=query_length / self.query.loadQuality_length()
		proportion_anchor=anchor_length / self.ancho.loadQuality_length()
		average_confidence=total_confidence / num_alignments

		self.quality=Quality(
			num_alignment=num_alignments,
			total_length=total_length,
			query_length=query_length,
			proportion_query=proportion_query,
			anchor_length=anchor_length,
			proportion_anchor=proportion_anchor,

			total_confidence=total_confidence,
			min_confidence=min_confidence,
			max_confidence=max_confidence,
			average_confidence=average_confidence,
			weighted_average_confidence=weighted_average_confidence
		)
		self.saveQualityObjectToFile()

	def getMem(self):
		return self.workspace.resources.getSmallMemory()
	def getTime(self):
		return self.workspace.resources.getSmallTime()
	def getThreads(self):
		return self.workspace.resources.getSmallThreads()

from Utils.Workspace import Workspace
from Operations.Step import Quality
from Operations.BioNano.Compare.Input import Input
from Operations.BioNano.Assemble.Merge import Merge
from Operations.BioNano.files import XmapFile
from collections import OrderedDict
from copy import copy
from collections import OrderedDict

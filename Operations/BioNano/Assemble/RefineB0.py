# Module: Assemble.BioNano.RefineB0
# Version: 0.1
# Author: Aaron Sharp
# Date: 07/14/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# prepare for the second step of refinement
from Operations.Step import Step
from collections import OrderedDict
from copy import copy

class RefineB0(Step):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters
		self.quality=None

		self.output_prefix="refineB0"
		self.color=1
		self.aligned_site_threshold=5
		self.max_coverage=100
		self.enable_multi_mode=True
		self.internal_split_ratio=0.20
		self.internal_trimmed_coverage_ratio=0.35
		# TODO this file doesn't exist in other assemblies...
		self.cnt_file="refineB0_max_id"
		self.min_contig_len=100.0
		self.allow_no_splits=True
		self.allow_infinite_splits=False
		self.min_end_coverage=6.99
		self.scale_bias_wt=0
		self.min_likelihood_ratio=1e2
		self.max_query_alignment=4
		self.max_reference_alignment=6
		self.max_repeat_shift=2
		self.repeat_pval_ratio=0.01
		self.repeat_log_pval_ratio=0.7
		self.repeat_min_shift_ratio=0.6
		self.min_gap_flanking_sites=2
		self.output_trimmed_coverage=True
		self.normalize_trimmed_coverage=True
		self.min_gap_flanking_len=55
		self.last_non_chimeric_site_after_gap=2
		self.split_molecules_with_outliers=True
		self.outlier_pvals_per_true_positive=1e-5
		self.end_outlier_prior_probability=1e-4
		self.pval_after_refinement=1
		self.faster_refinement_resolution=""
		self.count_splits_with_largest_ids=True
		self.contig_split_version=""
		self.reduced_contig_resolution_divided_by_two=2.0
		self.overwrite_output=True
		self.hash_window=5
		self.hash_min_sites=3
		self.hash_sd_max=2.4
		self.hash_sd_rms=1.5
		self.hash_relative_error=0.05
		self.hash_offset_kb=5.0
		self.hash_max_insert_errors=1
		self.hash_max_probe_errors=1
		self.hash_max_unresolved_sites=1
		self.hash_file=""
		self.hash_threshold=""
		self.hashdelta=10
		self.reduced_molecule_resolution=1.2
		self.insert_threads=4
		self.skip_alignment_statistic_computation=True
		self.sd=0.2
		self.sf=0.2
		self.sr=0.03
		self.res=3.3
		self.regex_acceptible_output_file=".*.bnx"
		self.write_output_to_file=True
		self.write_errors_to_file=True
		
		self.max_job_count=2
		self.autoGeneratePrereqs()

	def writeCode(self):
		code="cd " + self.workspace.work_dir + "\n"
		code+="mkdir -p " + self.getStepDir() + "\n"
		code+="cd " + self.getStepDir() + "\n"
		code+="pwd\n"

		param_values=OrderedDict()
		param_values["-i"]="placeholder"
		param_values["-o"]=self.output_prefix
		param_values["-maxthreads"]=str(self.getThreads())		 
		param_values["-ref"]=self.merge_refineA.getOutputFile()
		param_values["-T"]=str(self.vital_parameters.pval)
		param_values["-usecolor"]=str(self.color) 
		param_values["-A"]=str(self.aligned_site_threshold) 
		param_values["-extend"]="1"
		param_values["-MaxCov"]=str(self.max_coverage) 
		if self.enable_multi_mode: 
			param_values["-MultiMode"]=""
		param_values["-contigsplit"]=" ".join([str(self.internal_split_ratio), str(self.internal_trimmed_coverage_ratio), self.cnt_file])
		param_values["-MinSplitLen"]=str(self.min_contig_len) 
		param_values["-nosplit"] =  "2" if self.allow_no_splits else "0" if self.allow_infinite_splits else "1" 
		param_values["-EndTrim"]=str(self.min_end_coverage)
		param_values["-biaswt"]=str(self.scale_bias_wt) 
		param_values["-LRbias"]=str(self.min_likelihood_ratio) 
		param_values["-deltaX"]=str(self.max_query_alignment) 
		param_values["-deltaY"]=str(self.max_reference_alignment) 
		param_values["-RepeatMask"]=" ".join([str(self.max_repeat_shift), str(self.repeat_pval_ratio)]) 
		param_values["-RepeatRec"]=" ".join([str(self.repeat_log_pval_ratio), str(self.repeat_min_shift_ratio)])
		param_values["-CovTrim"]=str(self.min_gap_flanking_sites) 
		if self.output_trimmed_coverage:
			param_values["-ReplaceCov"]=""
		if self.normalize_trimmed_coverage:
			param_values["-TrimNorm"]=""
		param_values["-CovTrimLen"]=str(self.min_gap_flanking_len) 
		param_values["-TrimNormChim"]=str(self.last_non_chimeric_site_after_gap) 
		if self.split_molecules_with_outliers: 
			param_values["-TrimOutlier"]=""
		param_values["-outlier"]=str(self.outlier_pvals_per_true_positive) 
		param_values["-endoutlier"]=str(self.end_outlier_prior_probability) 
		param_values["-endoutlierFinal"]=str(self.pval_after_refinement) 
		param_values["-Mprobeval"]=str(self.faster_refinement_resolution) 
		if self.count_splits_with_largest_ids: 
			param_values["-splitcnt"]=""
		param_values["-splitrev"]=str(self.contig_split_version) 
		param_values["-rres"]=str(self.reduced_contig_resolution_divided_by_two) 
		if self.overwrite_output:
			param_values["-f"]=""
		param_values["-refine"]="0"
		param_values["-hashgen"] =  " ".join([str(self.hash_window), str(self.hash_min_sites), str(self.hash_sd_max), str(self.hash_sd_rms), str(self.hash_relative_error), str(self.hash_offset_kb), str(self.hash_max_insert_errors), str(self.hash_max_probe_errors), str(self.hash_max_unresolved_sites)]) 
		param_values["-hash"]=" ".join([self.hash_file, str(self.hash_threshold)]) 
		param_values["-hashdelta"]=str(self.hashdelta) 
		param_values["-mres"]=str(self.reduced_molecule_resolution) 
		param_values["-insertThreasds"]=str(self.insert_threads) 
		if self.skip_alignment_statistic_computation: 
			param_values["-nostat"]=""
		param_values["-maxmem"]=str(self.getMem())
		param_values["-FP"]=str(self.vital_parameters.fp)
		param_values["-FN"]=str(self.vital_parameters.fn)
		param_values["-sd"]=str(self.sd)
		param_values["-sf"]=str(self.sf)
		param_values["-sr"]=str(self.sr)
		param_values["-res"]=str(self.res)
		param_values["-refine"]="0"
		param_values["-grouped"]="../" + self.group_manifest.getOutputFile()
		param_values["-mapped"]="placeholder"
		param_values["-output-filter"]=self.regex_acceptible_output_file
		param_values["-id"]="placeholder"
		if self.write_output_to_file:
			param_values["-stdout"]=""
		if self.write_errors_to_file:
			param_values["-stderr"]=""
		param_values["-XmapStatRead"]="../"+self.molecule_stats.getOutputFile()
		param_values["-minlen"]=str(self.vital_parameters.min_molecule_len)
		param_values["-minsites"]=str(self.vital_parameters.min_molecule_sites)
		
		tmp_code=""
		cur_jobs=0
		code_parts=[]
		for block in xrange(1, self.split.vital_parameters.blocks+1):
			cur_jobs+=1
			param_values["-i"]=self.split.getOutputFile(block)
			param_values["-mapped"]="refineB0_id"+str(block)+"_mapped"
			param_values["-id"]=str(block)
			
			param_list=[self.workspace.binaries["bng_ref_aligner"]]
			for key in param_values:
				param_list.append(key)
				param_list.append(param_values[key])
			tmp_code+=" ".join(param_list) + "\n"

			if cur_jobs>=self.max_job_count:
				code_parts.append(code+tmp_code)
				tmp_code=""
				cur_jobs=0
		if len(tmp_code) > 0:
			code_parts.append(code+tmp_code)

		return code_parts

	def getStepDir(self):
		return "_".join(["refineB0", "fp"+str(self.vital_parameters.fp), "fn"+str(self.vital_parameters.fn), "pval"+str(self.vital_parameters.pval), "minlen"+str(self.vital_parameters.min_molecule_len), "minsites"+str(self.vital_parameters.min_molecule_sites)])

	def getOutputFile(self):
		return self.getStepDir() + "/" + self.output_prefix + "." + self.getOutputFileExtension()

	def getOutputFileExtension(self):
		return "contigs"
	def getOutputFileExtension(self):
		return "bnx"

	def autoGeneratePrereqs(self):
		self.inpt=Input(self.workspace)
		self.sort=Sort(self.workspace, copy(self.vital_parameters))
		self.molecule_stats=self.sort.getMoleculeStats()
		self.split=Split(self.workspace, copy(self.vital_parameters))
		self.split_summary=Summarize(self.workspace, self.split)
		self.pairwise_alignment=PairwiseAlignment(self.workspace, copy(self.vital_parameters))
		self.pairwise_summary=Summarize(self.workspace, self.pairwise_alignment)
		self.assembly=Assembly(self.workspace, copy(self.vital_parameters))
		self.assembly_summary=Summarize(self.workspace, self.assembly)
		self.merge_assembly=Merge(self.workspace, self.assembly)
		self.refineA=RefineA(self.workspace, copy(self.vital_parameters))
		self.refineA_summary=Summarize(self.workspace, self.refineA)
		self.merge_refineA=Merge(self.workspace, self.refineA)
		self.group_manifest=GroupManifest(self.workspace, self.refineA)
	
	def getPrereq(self):
		return self.group_manifest

	def getMem(self):
		return self.workspace.resources.getMediumMemory()
	def getTime(self):
		return self.workspace.resources.getLargeTime()
	def getThreads(self):
		return self.workspace.resources.getMediumThreads()

from Operations.BioNano.Assemble.Assembly import RefineA
from Operations.BioNano.Assemble.GroupManifest import GroupManifest
from Operations.BioNano.Assemble.Merge import Merge
from Operations.BioNano.Assemble.Summarize import Summarize
from Operations.BioNano.Assemble.Assembly import Assembly
from Operations.BioNano.Assemble.PairwiseAlignment import PairwiseAlignment
from Operations.BioNano.Assemble.Split import Split
from Operations.BioNano.Assemble.Sort import Sort
from Operations.BioNano.Assemble.Input import Input

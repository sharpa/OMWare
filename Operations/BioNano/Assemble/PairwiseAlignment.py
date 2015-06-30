# Module: Operations.BioNano.Assemble.PairwiseAlignment
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner to create a set of pairwise alignments
from Operations.Step import Step
from Operations.BioNano.Assemble.Sort import Sort
from Operations.BioNano.Assemble.Split import Split
from Operations.BioNano.Assemble.Summarize import Summarize
from collections import OrderedDict
from os import path

class PairwiseAlignment(Step):
	def __init__(self, workspace, vital_parameters):
		self.workspace=workspace
		self.vital_parameters=vital_parameters

		self.color=1
		self.sd=0.2
		self.sf=0.2
		self.sr=0.03
		self.res=3.3
		self.min_alignment_sites=5
		self.min_alignment_score=1
		self.outlier_pval=0.0001
		self.endoutlier_pval=0
		self.repeat_max_shift=2
		self.repeat_pval_change=0.01
		self.repeat_pval_ratio=0.7
		self.repeat_min_change=0.6
		self.hash_window=5
		self.hash_min_sites=3
		self.hash_sd_max=2.2
		self.hash_sd_rms=1.2
		self.hash_relative_error=0.05
		self.hash_offset_kb=3.0
		self.hash_max_insert_errors=1
		self.hash_max_probe_errors=1
		self.hash_max_unresolved_sites=1
		self.target_resolution=1.2
		self.allow_no_splits=True
		self.allow_infinite_splits=False
		self.overwrite_output=True
		self.send_output_to_file=True
		self.send_error_to_file=True

		split=Split(self.workspace, self.vital_parameters)
		total_blocks=split.total_job_count
		self.total_job_count=total_blocks*(total_blocks+1)/2 

		self.max_job_count=self.getTime() * (60.0/270.0) - 1
		if self.max_job_count<1:
			self.max_job_count=1

		self.autoGeneratePrereqs()

	def writeCode(self):
		code_parts=[]

		param_values=OrderedDict()
		param_values["-usecolor"] =  str(self.color)
		param_values["-FP"] =  str(self.vital_parameters.fp)
		param_values["-FN"] =  str(self.vital_parameters.fn)
		param_values["-sd"] =  str(self.sd)
		param_values["-sf"] =  str(self.sf)
		param_values["-sr"] =  str(self.sr)
		param_values["-res"] =  str(self.res)
		param_values["-T"] =  str(self.vital_parameters.pval)
		maxmem=int(self.getMem()/self.getThreads())
		if maxmem < 1:
			maxmem=1
		param_values["-maxmem"] =  str(maxmem)
		param_values["-o"] =  "placeholder"
		param_values["-A"] =  str(self.min_alignment_sites)
		param_values["-S"] =  str(self.min_alignment_score)
		param_values["-outlier"] =  str(self.outlier_pval)
		param_values["-endoutlier"] =  str(self.endoutlier_pval)
		param_values["-RepeatMask"] =  " ".join([str(self.repeat_max_shift), str(self.repeat_pval_change)])
		param_values["-RepeatRec"] =  " ".join([str(self.repeat_pval_ratio), str(self.repeat_min_change)])
		param_values["-hashgen"] =  " ".join([str(self.hash_window), str(self.hash_min_sites), str(self.hash_sd_max), str(self.hash_sd_rms), str(self.hash_relative_error), str(self.hash_offset_kb), str(self.hash_max_insert_errors), str(self.hash_max_probe_errors), str(self.hash_max_unresolved_sites)])
		param_values["-hash"] =  ""
		param_values["-mres"] =  str(self.target_resolution)
		param_values["-nosplit"] =  "2" if self.allow_no_splits else "0" if self.allow_infinite_splits else "1"
		param_values["-maxthreads"] =  str(self.getThreads())
		param_values["-XmapStatRead"] =  "../" + str(self.molecule_stats.getOutputFile())

		if self.overwrite_output:
			param_values["-f"]=""
		if self.send_output_to_file:
			param_values["-stdout"]=""
		if self.send_error_to_file:
			param_values["-stderr"]=""
		
		tmp_code=""
		cur_jobs=0
		totalBlocks=self.split.total_job_count
		currentJob = 0
		for i in xrange(1,totalBlocks+1):
			file1="../" + self.split.getOutputFile(i)
			for j in range(i,totalBlocks + 1):
				file2="../" + self.split.getOutputFile(j)

				currentJob += 1
				param_values["-o"]='pairwise%dof%d' % (currentJob, self.total_job_count)
				if path.exists(self.getStepDir() + "/" + param_values["-o"] + ".align"):
					continue

				param_values["-i"]=file1
				if i==j :
					if "-first" in param_values:
						del param_values["-first"]
					if "-1" in param_values:
						del param_values["-1"]
					if "-i " in param_values:
						del param_values["-i "]
				else :
					param_values["-first"]=""
					param_values["-1"]=""
					param_values["-i "]=file2

				param_list=[self.workspace.binaries["bng_ref_aligner"]]
				for key in param_values:
					param_list.append(key)
					param_list.append(param_values[key])
				tmp_code += "if [ ! -e " + param_values["-o"] + ".align ]\n"
				tmp_code += "then\n"
				tmp_code += "  " + " ".join(param_list) + "\n"
				tmp_code += "fi\n"

				cur_jobs+=1
				if cur_jobs>=self.max_job_count:
					code = "cd " + self.workspace.work_dir + "\n"
					code += "mkdir -p " + self.getStepDir() + "\n"
					code += "cd " + self.getStepDir() + "\n"
					code += tmp_code
					code_parts.append(code)

					tmp_code=""
					cur_jobs=0
		if tmp_code != "":
			code = "cd " + self.workspace.work_dir + "\n"
			code += "mkdir -p " + self.getStepDir() + "\n"
			code += "cd " + self.getStepDir() + "\n"
			code += "pwd\n"
			code += tmp_code
			code_parts.append(code)

			tmp_code=""
			cur_jobs=0

		if len(code_parts)==0:
			return ["# do nothing"]
		return code_parts

	def getStepDir(self):
		return "_".join(["pairwise", self.workspace.input_file, "fp"+str(self.vital_parameters.fp), "fn"+str(self.vital_parameters.fn), "pval"+str(self.vital_parameters.pval)])

	def autoGeneratePrereqs(self):
		self.sort=Sort(self.workspace, self.vital_parameters)
		self.split=Split(self.workspace, self.vital_parameters)
		self.molecule_stats=self.sort.getMoleculeStats()

	def getPrereqs(self):
		return [Summarize(self.workspace, self.split)]

	def getMem(self):
		return self.workspace.resources.getLargeMemory()
	def getTime(self):
		return self.workspace.resources.getLargeTime()
	def getThreads(self):
		return self.workspace.resources.getLargeThreads()

	def getListFile(self):
		return self.getStepDir() + "/align.list"
	def getOutputFileExtension(self):
		return "align"


# Module: UnitTests.SmokeTest.py
# Version: 0.1
# Author: Aaron Sharp
# Date: 07/23/2015
# 
# The purpose of this module is to provide integration tests for 
# all modules in  Operations.Assemble.BioNano
import unittest
import os
from copy import copy
import shutil
import StringIO
import sys
import re
from Utils.Workspace import Workspace
from Operations.SBATCHCodeFormatter import CodeFormatter
from Operations.BioNano.Assemble.Assembly import Assembly
from Operations.BioNano.Assemble.PairwiseAlignment import PairwiseAlignment
from Operations.BioNano.Assemble.Split import Split
from Operations.BioNano.Assemble.Sort import Sort
from Operations.BioNano.Assemble.VitalParameters import VitalParameters
from Operations.BioNano.Parameterize.ParameterSearch import ParameterSearch

class SmokeTest(unittest.TestCase):
	vital_parameters=VitalParameters(1.5, .150, 1e-5, 100, 6)
	formatter=CodeFormatter()
	native_stdout=sys.stdout
	saved_path=os.getcwd()
	def setUp(self):
		self.workspace=Workspace(self.saved_path + "/test_work_dir", "input.bnx")
		os.mkdir(self.workspace.work_dir)
		os.chdir(self.workspace.work_dir)
		with open(self.workspace.input_file, "w") as bnx_file:
			bnx_file.write("\n".join([
				"# BNX File Version:	1.2", 
				"#0h	LabelChannel	MoleculeId	Length	AvgIntensity	SNR	NumberofLabels	OriginalMoleculeId	ScanNumber	ScanDirection	ChipId	Flowcell	RunId	GlobalScanNumber",
				"#0f	int	int	float	float	float	int	int	int	int	string	int	int	int",
				"#1h	LabelChannel	LabelPositions[N]",
				"#1f	int	float",
				"#2h	LabelChannel	LabelPositions[N]",
				"#2h	int	float",
				"#Qh	QualityScoreID	QualityScores[N]",
				"#Qf	str	float",
				"0	1	11915.3	0.064331	39.060	7	1	1	-1	20249,11731,11/25/2013,840012494	1	1	1",
				"1	0.0	3785.6	5068.4	7060.8	7968.7	7987.8	11267.0	11915.3",
				"QX11	0.6905	0.8113	0.5751	1.4108	2.2148	1.1966	0.8701",
				"QX12	0.0327	0.0330	0.0328	0.0342	0.0349	0.0341	0.0334"
			]))
		self.workspace.addBinary("bng_assembler", "path/to/Assembler")
		self.workspace.addBinary("bng_ref_aligner", "path/to/RefAligner")

		self.buffer_stdout=StringIO.StringIO()
		sys.stdout=self.buffer_stdout

	def tearDown(self):
		self.buffer_stdout.close()
		sys.stdout=self.native_stdout

		os.chdir(self.saved_path)
		shutil.rmtree(self.workspace.work_dir)

	def dummy_returnTrue(self):
		return True
	def dummy_returnFalse(self):
		return False

	def test_writeCode_sort(self):
		step=Sort(self.workspace, copy(self.vital_parameters))
		expected="\n".join(["#!/bin/bash",
			"",
			"",
			"step1=\"-d afterok\"",
			"sresult=`sbatch  step1_part1.sh`",
			"echo $sresult",
			"sid=`echo $sresult | awk '{print $NF}'`",
			"step1=$step1:$sid",
			""
			])

		self.formatter.runOneStep(step)

		self.assertEqual(expected, self.buffer_stdout.getvalue())

	def test_writeCode_sort_isComplete(self):
		native_isComplete=Sort.isComplete
		Sort.isComplete=self.dummy_returnTrue.im_func
		step=Sort(self.workspace, copy(self.vital_parameters))
		expected="\n".join(["#!/bin/bash",
			"",
			""
			])


		self.formatter.runOneStep(step)

		Sort.isComplete=native_isComplete

		self.assertEqual(expected, self.buffer_stdout.getvalue())

	def test_writeCode_assembly(self):
		step=Assembly(self.workspace, copy(self.vital_parameters))
		
		expected="\n".join(["#!/bin/bash",
				"",
				"",
				"step1=\"-d afterok\"",
				"sresult=`sbatch  step1_part1.sh`",
				"echo $sresult",
				"sid=`echo $sresult | awk '{print $NF}'`",
				"step1=$step1:$sid",
				"",
				"step2=\"-d afterok\"",
				"sresult=`sbatch $step1 step2_part1.sh`",
				"echo $sresult",
				"sid=`echo $sresult | awk '{print $NF}'`",
				"step2=$step2:$sid",
				"",
				"step3=\"-d afterok\"",
				"sresult=`sbatch $step2 step3_part1.sh`",
				"echo $sresult",
				"sid=`echo $sresult | awk '{print $NF}'`",
				"step3=$step3:$sid",
				"",
				"step4=\"-d afterok\"",
				"sresult=`sbatch $step3 step4_part1.sh`",
				"echo $sresult",
				"sid=`echo $sresult | awk '{print $NF}'`",
				"step4=$step4:$sid",
				"",
				"step5=\"-d afterok\"",
				"sresult=`sbatch $step4 step5_part1.sh`",
				"echo $sresult",
				"sid=`echo $sresult | awk '{print $NF}'`",
				"step5=$step5:$sid",
				"",
				"step6=\"-d afterok\"",
				"sresult=`sbatch $step5 step6_part1.sh`",
				"echo $sresult",
				"sid=`echo $sresult | awk '{print $NF}'`",
				"step6=$step6:$sid",
				""
				])
		
		self.formatter.runOneStep(step)

		self.assertEqual(expected, self.buffer_stdout.getvalue())

	def test_parameterSearch(self):
		search=ParameterSearch(self.workspace, 900)
		
		expected_lines={
			"total": 2559,
			"blank": 428,
			"level6": 405,
			"sbatch_$level5": 405,
			"level5": 9,
			"sbatch_$level4": 9,
			"level4": 9,
			"sbatch_$level3": 9,
			"level3": 1,
			"sbatch_$level2": 1,
			"level2": 1,
			"sbatch_$level1": 1,
			"level1": 1,
			"sbatch__level1": 1
		}
		BLANK=re.compile("^$")
		LEVEL6=re.compile("level6_.*=\"-d afterok\"")
		LEVEL5=re.compile("level5_.*=\"-d afterok\"")
		LEVEL4=re.compile("level4_.*=\"-d afterok\"")
		LEVEL3=re.compile("level3_.*=\"-d afterok\"")
		LEVEL2=re.compile("level2_.*=\"-d afterok\"")
		LEVEL1=re.compile("level1_.*=\"-d afterok\"")
		SBATCH_LEVEL5=re.compile("sbatch \$level5")
		SBATCH_LEVEL4=re.compile("sbatch \$level4")
		SBATCH_LEVEL3=re.compile("sbatch \$level3")
		SBATCH_LEVEL2=re.compile("sbatch \$level2")
		SBATCH_LEVEL1=re.compile("sbatch \$level1")
		SBATCH_NADA=re.compile("sbatch  level1_")

		self.formatter.runSeveralSteps(search.writeCode())

		actual_lines={
			"total": 0,
			"blank": 0,
			"level6": 0,
			"sbatch_$level5": 0,
			"level5": 0,
			"sbatch_$level4": 0,
			"level4": 0,
			"sbatch_$level3": 0,
			"level3": 0,
			"sbatch_$level2": 0,
			"level2": 0,
			"sbatch_$level1": 0,
			"level1": 0,
			"sbatch__level1": 0
		}
		output=self.buffer_stdout.getvalue()
		for line in output.split("\n"):
			actual_lines["total"]+=1
			if BLANK.search(line) is not None:
				actual_lines["blank"]+=1
			if LEVEL6.search(line) is not None:
				actual_lines["level6"]+=1
			if LEVEL5.search(line) is not None:
				actual_lines["level5"]+=1
			if LEVEL4.search(line) is not None:
				actual_lines["level4"]+=1
			if LEVEL3.search(line) is not None:
				actual_lines["level3"]+=1
			if LEVEL2.search(line) is not None:
				actual_lines["level2"]+=1
			if LEVEL1.search(line) is not None:
				actual_lines["level1"]+=1
			if SBATCH_LEVEL5.search(line) is not None:
				actual_lines["sbatch_$level5"]+=1
			if SBATCH_LEVEL4.search(line) is not None:
				actual_lines["sbatch_$level4"]+=1
			if SBATCH_LEVEL3.search(line) is not None:
				actual_lines["sbatch_$level3"]+=1
			if SBATCH_LEVEL2.search(line) is not None:
				actual_lines["sbatch_$level2"]+=1
			if SBATCH_LEVEL1.search(line) is not None:
				actual_lines["sbatch_$level1"]+=1
			if SBATCH_NADA.search(line) is not None:
				actual_lines["sbatch__level1"]+=1

		self.maxDiff=None
		self.assertEqual(expected_lines, actual_lines)


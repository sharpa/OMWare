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
from Utils.Workspace import Workspace
from Operations.SBATCHCodeFormatter import CodeFormatter
from Operations.BioNano.Assemble.Assembly import Assembly
from Operations.BioNano.Assemble.PairwiseAlignment import PairwiseAlignment
from Operations.BioNano.Assemble.Split import Split
from Operations.BioNano.Assemble.Sort import Sort
from Operations.BioNano.Assemble.VitalParameters import VitalParameters

class SmokeTest(unittest.TestCase):
	workspace=Workspace("test_work_dir", "input.bnx")
	vital_parameters=VitalParameters(1.5, .150, 1e-5, 100, 6)
	formatter=CodeFormatter()
	native_stdout=sys.stdout
	def setUp(self):
		os.mkdir(self.workspace.work_dir)
		with open(self.workspace.work_dir + "/" + self.workspace.input_file, "w") as bnx_file:
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

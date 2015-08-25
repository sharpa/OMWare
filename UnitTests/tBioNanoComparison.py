# Module: UnitTests.tBioNanoComparison.py
# Version: 0.1
# Author: Aaron Sharp
# Date: 08/24/2015
# 
# The purpose of this module is to provide unit tests for 
# all modules in  Operations.BioNano.Compare

import unittest
from Operations.BioNano.Compare.Input import Input
from Operations.BioNano.files import CmapFile
from Operations.BioNano.Compare.ReferenceAlignment import ReferenceAlignment
from Utils.Workspace import Workspace
from UnitTests.Helper import Mock

class tInput(unittest.TestCase):
	workspace=Mock(input_file="input_file", work_dir="work_dir")
	def setUp(self):
		self.obj=Input(self.workspace)
	def test_init(self):
		expected=Mock(workspace=self.workspace, quality=None)
		self.assertEqual(expected, self.obj)

	def test_hash(self):
		self.assertEqual(hash((self.workspace.input_file, self.workspace.work_dir, "Input")), self.obj.__hash__())

	def test_str(self):
		expected="Input: " + self.workspace.input_file
		self.assertEqual(expected, self.obj.__str__())

	def test_eq_None(self):
		other=None
		expected=[False, True]
		actual=[]

		actual.append(self.obj==other)
		actual.append(self.obj!=other)

		self.assertEqual(expected, actual)

	def test_eq_diffClass(self):
		other=Mock(workspace=self.workspace)
		expected=[False, True]
		actual=[]

		actual.append(self.obj==other)
		actual.append(self.obj!=other)

		self.assertEqual(expected, actual)

	def test_eq_diffWorkspace(self):
		other=Input(Mock(input_file="other_input_file", work_dir="other_work_dir"))
		expected=[False, True]
		actual=[]

		actual.append(self.obj==other)
		actual.append(self.obj!=other)

		self.assertEqual(expected, actual)

	def test_eq_equal(self):
		other=Input(self.workspace)
		expected=[True, False]
		actual=[]

		actual.append(self.obj==other)
		actual.append(self.obj!=other)

		self.assertEqual(expected, actual)

	def test_writeCode(self):
		self.assertEqual([], self.obj.writeCode())

	def test_getStepDir(self):
		self.assertEqual(self.workspace.input_file, self.obj.getStepDir())

	def test_getOutputFile(self):
		self.assertEqual(self.workspace.input_file, self.obj.getOutputFile())

	def test_getOutputFileExtension(self):
		expected=CmapFile.getExtension()
		actual=self.obj.getOutputFileExtension()
	
		self.assertEqual(expected, actual)

	def test_autoGeneratePrereqs(self):
		actual=Input(self.workspace)
		actual.autoGeneratePrereqs()

		self.assertEqual(self.obj, actual)

	def test_getPrereqs(self):
		self.assertEqual(None, self.obj.getPrereq())

	def test_getMem(self):
		self.assertEqual(-1, self.obj.getMem())

	def test_getTime(self):
		self.assertEqual(-1, self.obj.getTime())
	def test_getThreads(self):
		self.assertEqual(-1, self.obj.getThreads())

class tReferenceAlignment(unittest.TestCase):
	workspace=Mock(input_file="input_file", work_dir="work_dir")
	merge=Mock()
	ref_file="ref_file"
	def setUp(self):
		native_autoGen=ReferenceAlignment.autoGeneratePrereqs
		ReferenceAlignment.autoGeneratePrereqs=self.dummy_autoGen.im_func

		self.obj=ReferenceAlignment(self.workspace, self.merge, self.ref_file)

		ReferenceAlignment.autoGeneratePrereqs=native_autoGen

	def dummy_autoGen(self):
		self.autoGenCalled=True
	def dummy_getString(self):
		return "string"
	def dummy_getNum(self):
		return -1

	def test_init(self):
		native_autoGen=ReferenceAlignment.autoGeneratePrereqs
		ReferenceAlignment.autoGeneratePrereqs=self.dummy_autoGen.im_func

		expected=ReferenceAlignment("dummy_workspace", "dummy_merge", "dummy_ref_file")
		expected.workspace=self.workspace
		expected.merge=self.merge
		expected.ref_file=self.ref_file
		expected.quality=None
		expected.autoGenCalled=True
		expected.output_prefix=self.ref_file
		expected.send_output_to_file=True
		expected.send_error_to_file=True
		expected.output_veto_regex="_intervals.txt$"
		expected.res=2.9
		expected.pval=1e-10
		expected.fp=0.6 
		expected.fn=0.06
		expected.sf=0.20
		expected.sd=0.10
		expected.allow_overhang=True
		expected.outlier_pval=0.0001
		expected.end_outlier_pval=0.001
		expected.max_query_alignment_interval=12
		expected.max_reference_alignment_interval=12
		expected.min_sites_for_chimera=14
		expected.hash_window=5
		expected.hash_min_sites=3
		expected.hash_sd_max=2.2
		expected.hash_sd_rms=1.2
		expected.hash_relative_error=0.05
		expected.hash_offset_kb=3.0
		expected.hash_max_insert_errors=1
		expected.hash_max_probe_errors=1
		expected.hash_max_unresolved_sites=1
		expected.hash_delta=50
		expected.target_resolution=1e-3
		expected.resolution_reduction=1.2
		expected.allow_no_splits=True
		expected.allow_infinite_splits=False
		expected.scale_bias_wt=0
		expected.overwrite_output=True
		expected.print_indel_file=True

		ReferenceAlignment.autoGeneratePrereqs=native_autoGen

		self.assertEqual(expected, self.obj)

	def test_hash(self):
		self.assertEqual(hash((self.workspace.input_file, self.workspace.work_dir, self.ref_file)), self.obj.__hash__())

	def test_str(self):
		self.assertEqual("Comparison of " + self.workspace.input_file + " to " + self.ref_file, self.obj.__str__())

	def test_writeCode(self):
		native_getStepDir=ReferenceAlignment.getStepDir
		ReferenceAlignment.getStepDir=self.dummy_getString.im_func
		Mock.getOutputFile=self.dummy_getString.im_func
		self.obj.anchor=Mock()
		self.obj.query=Mock()
		native_getThreads=ReferenceAlignment.getThreads
		ReferenceAlignment.getThreads=self.dummy_getNum.im_func
		native_getMem=ReferenceAlignment.getMem
		ReferenceAlignment.getMem=self.dummy_getNum.im_func
		self.workspace.binaries={"bng_ref_aligner": "RefAligner"}

		expected=["cd work_dir\nmkdir string\ncd string\npwd\nRefAligner -ref ../string -i ../string -o ref_file -maxthreads -1 -insertThreads -1 -maxmem 1 -output-veto-filter _intervals.txt$ -res 2.9 -T 1e-10 -FP 0.6 -FN 0.06 -sf 0.2 -sd 0.1 -extend 1 -outlier 0.0001 -endoutlier 0.001 -deltaX 12 -deltaY 12 -xmapchim 14 -hashgen 5 3 2.2 1.2 0.05 3.0 1 1 1 -hash  -hashdelta 50 -mres 0.001 -rres 1.2 -nosplit 2 -biaswt 0 -stdout  -stderr  -force  -indel "]
		actual=self.obj.writeCode()

		ReferenceAlignment.getStepDir=native_getStepDir
		del Mock.getOutputFile
		ReferenceAlignment.getThreads=native_getThreads
		ReferenceAlignment.getMem=native_getMem
		del self.workspace.binaries

		self.assertEqual(expected, actual)

	def test_getStepDir(self):
		self.assertEqual("comparison_" + self.workspace.input_file + "_" + self.ref_file, self.obj.getStepDir())

	def test_getOutputFile(self):
		native_getStepDir=ReferenceAlignment.getStepDir
		ReferenceAlignment.getStepDir=self.dummy_getString.im_func
		self.obj.output_prefix="prefix"
		native_getOutputFileExtension=ReferenceAlignment.getOutputFileExtension
		ReferenceAlignment.getOutputFileExtension=self.dummy_getString.im_func

		expected=self.dummy_getString() + "/prefix." + self.dummy_getString()
		actual=self.obj.getOutputFile()

		ReferenceAlignment.getStepDir=native_getStepDir
		ReferenceAlignment.getOutputFileExtension=native_getOutputFileExtension

		self.assertEqual(expected, actual)

	def test_getOutputFileExtension(self):
		self.assertEqual("xmap", self.obj.getOutputFileExtension())

	def test_autoGeneratePrereqs(self):
		Mock.getOutputFile=self.dummy_getString.im_func
		self.obj.anchor=Input(Workspace(self.workspace.work_dir, self.ref_file))
		self.obj.query=Input(Workspace(self.workspace.work_dir, self.dummy_getString()))

		actual=ReferenceAlignment(self.workspace, self.merge, self.ref_file)
		actual.autoGenCalled=True

		del Mock.getOutputFile

		self.assertEqual(self.obj, actual)

	def test_getPrereq(self):
		self.assertEqual(self.merge, self.obj.getPrereq())

	def test_getMem(self):
		Mock.getSmallMemory=self.dummy_getNum.im_func
		self.workspace.resources=Mock()

		expected=self.dummy_getNum()
		actual=self.obj.getMem()

		del Mock.getSmallMemory
		del self.workspace.resources

		self.assertEqual(expected, actual)

	def test_getTime(self):
		Mock.getSmallTime=self.dummy_getNum.im_func
		self.workspace.resources=Mock()

		expected=self.dummy_getNum()
		actual=self.obj.getTime()

		del Mock.getSmallTime
		del self.workspace.resources

		self.assertEqual(expected, actual)

	def test_getThreads(self):
		Mock.getSmallThreads=self.dummy_getNum.im_func
		self.workspace.resources=Mock()

		expected=self.dummy_getNum()
		actual=self.obj.getThreads()

		del Mock.getSmallThreads
		del self.workspace.resources

		self.assertEqual(expected, actual)

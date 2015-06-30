# Module: UnitTests.tBioNanoAssembly.py
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/29/2015
# 
# The purpose of this module is to provide unit tests for 
# all modules in  Operations.Assemble.BioNano
import unittest
import UnitTests.Helper
from Operations.BioNano.Assemble.Assembly import Assembly
from Operations.BioNano.Assemble.Summarize import Summarize
from Operations.BioNano.Assemble.Sort import Sort
from Operations.BioNano.Assemble.Split import Split
from Operations.BioNano.Assemble.PairwiseAlignment import PairwiseAlignment
from Operations.BioNano.Assemble.MoleculeStats import MoleculeStats

class tAssembly(unittest.TestCase):
	workspace=UnitTests.Helper.Mock(input_file="input_file", work_dir="work_dir")
	vital_parameters=UnitTests.Helper.Mock(pval="pval", fp="fp", fn="fn", min_molecule_len="minlen", min_molecule_sites="minsites")
	native_autoGeneratePrereqs=Assembly.autoGeneratePrereqs

	def dummy_autoGeneratePrereqs(self):
		self.autoGeneratePrereqsCalled=True

	def setUp(self):
		Assembly.autoGeneratePrereqs=tAssembly.dummy_autoGeneratePrereqs.im_func
		self.obj=Assembly(self.workspace, self.vital_parameters)

	def tearDown(self):
		Assembly.autoGeneratePrereqs=self.native_autoGeneratePrereqs

	def test_default_init(self):
		expectedDefault=Assembly(None, None)
		expectedDefault.workspace=self.workspace
		expectedDefault.vital_parameters=self.vital_parameters

		expectedDefault.sd=0.2
		expectedDefault.sf=0.2
		expectedDefault.sr=0.03
		expectedDefault.res=3.3
		expectedDefault.color=1
		expectedDefault.alignment_score_threshold=1
		expectedDefault.max_rel_coverage_multiple=100
		expectedDefault.max_rel_coverage_absolute=200
		expectedDefault.max_rel_coverage_absolute_2=30
		expectedDefault.bulge_coverage=20
		expectedDefault.max_coverage=10
		expectedDefault.min_coverage=10
		expectedDefault.min_average_coverage=5
		expectedDefault.min_maps=5
		expectedDefault.min_contig_len=0.0
		expectedDefault.end_trim=1
		expectedDefault.chimera_pval=0.001
		expectedDefault.chimera_num=3
		expectedDefault.fast_bulge=1000
		expectedDefault.fragile_preserve=False
		expectedDefault.draftsize=1
		expectedDefault.min_duplicate_len=1
		expectedDefault.binary_output=True
		expectedDefault.min_snr=2
		expectedDefault.output_prefix="unrefined"
		expectedDefault.add_alignment_filter=True
		expectedDefault.alignment_filter_threshold=100
		expectedDefault.alignment_filter_minlen_change=2.0
		expectedDefault.alignment_filter_pval_change=0.5
		expectedDefault.overwrite_output=True
		expectedDefault.hide_branches=True
		expectedDefault.send_output_to_file=True
		expectedDefault.send_errors_to_file=True

		expectedDefault.autoGeneratePrereqsCalled=True

		self.assertEqual(expectedDefault, self.obj)
		
	def test_default_write_code(self):
		expectedCode=""

		self.assertEqual(expectedCode(self.obj.writeCode()))

	def dummy_inputDotGetStepDir(self):
		return "input_file"

	def test_default_get_step_dir(self):
		UnitTests.Helper.Mock.getStepDir=tAssembly.dummy_inputDotGetStepDir.im_func
		self.obj.inpt=UnitTests.Helper.Mock()
		self.assertEqual("assembly_input_file_fpfp_fnfn_pvalpval_minlenminlen_minsitesminsites",self.obj.getStepDir())
		del UnitTests.Helper.Mock.getStepDir

	def dummy_getStepDir(self):
		return "dummy"
	def test_get_output_file(self):
		native_getStepDir=Assembly.getStepDir
		Assembly.getStepDir=tAssembly.dummy_getStepDir.im_func
		self.obj.output_prefix="dummy"

		self.assertEqual("dummy/dummy.contigs",self.obj.getOutputFile())

		Assembly.getStepDir=native_getStepDir

	def test_get_output_file_extension(self):
		self.assertEqual("contigs",self.obj.getOutputFileExtension())

	def test_auto_generate_prereqs(self):
		self.assertEqual(1,2)

	def test_get_prereqs(self):
		pairwise=UnitTests.Helper.Mock()
		self.obj.pairwise_alignment=pairwise

		self.assertEqual([Summarize(self.workspace, pairwise)],self.obj.getPrereqs())

	def dummy_getLargeMemory(self):
		return -1
	def test_get_mem(self):
		UnitTests.Helper.Mock.getLargeMemory=tAssembly.dummy_getLargeMemory.im_func
		self.workspace.resources=UnitTests.Helper.Mock()

		self.assertEqual(self.dummy_getLargeMemory(), self.obj.getMem())

		del UnitTests.Helper.Mock.getLargeMemory
		del self.workspace.resources

	def dummy_getMediumTime(self):
		return -1
	def test_get_time(self):
		UnitTests.Helper.Mock.getMediumTime=tAssembly.dummy_getMediumTime.im_func
		self.workspace.resources=UnitTests.Helper.Mock()

		self.assertEqual(self.dummy_getMediumTime(), self.obj.getTime())

		del UnitTests.Helper.Mock.getMediumTime
		del self.workspace.resources

	def test_get_threads(self):
		self.assertEqual(1, self.obj.getThreads())

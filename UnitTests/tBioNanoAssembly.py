# Module: UnitTests.tBioNanoAssembly.py
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/29/2015
# 
# The purpose of this module is to provide unit tests for 
# all modules in  Operations.Assemble.BioNano
import unittest
import os
from collections import OrderedDict
from copy import copy
from UnitTests.Helper import Mock
from Operations.BioNano.files import BnxFile
from Operations.BioNano.Assemble.RefineB0 import RefineB0
from Operations.BioNano.Assemble.Assembly import RefineA
from Operations.BioNano.Assemble.Assembly import Assembly
from Operations.BioNano.Assemble.Assembly import GenericAssembly
from Operations.BioNano.Assemble.Summarize import Summarize
from Operations.BioNano.Assemble.Merge import Merge
from Operations.BioNano.Assemble.GroupManifest import GroupManifest
from Operations.BioNano.Assemble.Sort import Sort
from Operations.BioNano.Assemble.Split import Split
from Operations.BioNano.Assemble.PairwiseAlignment import PairwiseAlignment
from Operations.BioNano.Assemble.MoleculeStats import MoleculeStats
from Operations.BioNano.Assemble.Input import Input

class tAssembly(unittest.TestCase):
	workspace=Mock(input_file="input_file", work_dir="work_dir")
	vital_parameters=Mock(pval=1e-5, fp=1.5, fn=.150, min_molecule_len=100, min_molecule_sites=6)
	native_autoGeneratePrereqs=Assembly.autoGeneratePrereqs

	def dummy_autoGeneratePrereqs(self):
		self.autoGeneratePrereqsCalled=True
	def dummy_getResources(self):
		return -1
	def dummy_getOutputFile(self):
		return "output_file"

	def setUp(self):
		Assembly.autoGeneratePrereqs=tAssembly.dummy_autoGeneratePrereqs.im_func
		self.obj=Assembly(self.workspace, self.vital_parameters)

	def tearDown(self):
		Assembly.autoGeneratePrereqs=self.native_autoGeneratePrereqs

	def test_default_init(self):
		expectedDefault=Assembly(None, None)
		expectedDefault.workspace=self.workspace
		expectedDefault.vital_parameters=self.vital_parameters
		expectedDefault.quality=None

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

		expectedDefault.total_job_count=1

		expectedDefault.autoGeneratePrereqsCalled=True

		self.assertEqual(expectedDefault, self.obj)
		
	def test_default_write_code(self):
		self.workspace.binaries={"bng_assembler": "Assembler"}
		native_getStepDir=Assembly.getStepDir
		Assembly.getStepDir=self.dummy_getStepDir.im_func
		native_getMem=Assembly.getMem
		Assembly.getMem=self.dummy_getResources.im_func
		native_getThreads=Assembly.getThreads
		Assembly.getThreads=self.dummy_getResources.im_func
		Mock.getOutputFile=self.dummy_getOutputFile.im_func
		self.obj.split_summary=Mock()
		self.obj.pairwise_summary=Mock()
		self.obj.molecule_stats=Mock()
		
		expected=["cd " + self.workspace.work_dir + "\n" +
			"mkdir " + self.dummy_getStepDir() + "\n" +
			"cd " + self.dummy_getStepDir() + "\n" +
			"pwd\n" +
			"Assembler -if ../" + self.dummy_getOutputFile() + " -af ../" + self.dummy_getOutputFile() + " -XmapStatRead ../" + self.dummy_getOutputFile() + " -usecolor 1 -FP " + str(self.vital_parameters.fp) + " -FN " + str(self.vital_parameters.fn) + " -sd 0.2 -sf 0.2 -sr 0.03 -res 3.3 -T " + str(self.vital_parameters.pval) + " -S 1 -MaxRelCoverage 100 200 30 -BulgeCoverage 20 -MaxCoverage 10 -MinCov 10 -MinAvCov 5 -MinMaps 5 -MinContigLen 0.0 -EndTrim 1 -refine 0 -PVchim 0.001 3 -FastBulge 1000 -FragilePreserve 0 -draftsize 1 -SideBranch 1 -contigs_format 1 -maxthreads " + str(self.dummy_getResources()) + " -maxmem 1 -minlen " + str(self.vital_parameters.min_molecule_len) + " -minsites " + str(self.vital_parameters.min_molecule_sites) + " -minSNR 2 -o unrefined -AlignmentFilter 100 2.0 0.5 -force  -SideChain  -stdout  -stderr \n"]

		actual=self.obj.writeCode()

		del self.workspace.binaries
		Assembly.getStepDir=native_getStepDir
		Assembly.getMem=native_getMem
		Assembly.getThreads=native_getThreads
		del Mock.getOutputFile

		self.assertEqual(expected, actual)

	def dummy_inputDotGetStepDir(self):
		return "input_file"

	def test_default_get_step_dir(self):
		Mock.getStepDir=tAssembly.dummy_inputDotGetStepDir.im_func
		self.obj.inpt=Mock()
		self.assertEqual("assembly_input_file_fp" + str(self.vital_parameters.fp) + "_fn" + str(self.vital_parameters.fn) + "_pval" + str(self.vital_parameters.pval) + "_minlen" + str(self.vital_parameters.min_molecule_len) + "_minsites" + str(self.vital_parameters.min_molecule_sites),self.obj.getStepDir())
		del Mock.getStepDir

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
		expected=Assembly(self.workspace, self.vital_parameters)
		Assembly.autoGeneratePrereqs=self.native_autoGeneratePrereqs
		native_getTime_split=Split.getTime
		Split.getTime=self.dummy_getLargeMemory.im_func
		native_getTime_pairwise=PairwiseAlignment.getTime
		PairwiseAlignment.getTime=self.dummy_getLargeMemory.im_func
		self.obj.vital_parameters.blocks=1
		self.vital_parameters.blocks=1

		expected.inpt=Input(self.workspace)
		expected.sort=Sort(self.workspace, copy(self.vital_parameters))
		expected.molecule_stats=expected.sort.getMoleculeStats()
		expected.split=Split(self.workspace, copy(self.vital_parameters))
		expected.split_summary=Summarize(self.workspace, expected.split)
		expected.pairwise_alignment=PairwiseAlignment(self.workspace, copy(self.vital_parameters))
		expected.pairwise_summary=Summarize(self.workspace, expected.pairwise_alignment)

		self.obj.autoGeneratePrereqs()

		Split.getTime=native_getTime_split
		PairwiseAlignment.getTime=native_getTime_pairwise
		del self.obj.vital_parameters.blocks

		self.assertEqual(expected, self.obj)

	def test_get_prereq(self):
		pairwise_summary=Mock()
		self.obj.pairwise_summary=pairwise_summary

		self.assertEqual(pairwise_summary,self.obj.getPrereq())

	def test_isComplete_is(self):
		native_getOutputFile=Assembly.getOutputFile
		Assembly.getOutputFile=self.dummy_getOutputFile.im_func
		with open(self.dummy_getOutputFile(), "w"):

			actual = self.obj.isComplete()

		os.remove(self.dummy_getOutputFile())
		Assembly.getOutputFile=native_getOutputFile

		self.assertTrue(actual)

	def test_isComplete_isNot(self):
		native_getOutputFile=Assembly.getOutputFile
		Assembly.getOutputFile=self.dummy_getOutputFile.im_func

		actual = self.obj.isComplete()
		Assembly.getOutputFile=native_getOutputFile

		self.assertFalse(actual)

	def dummy_returnFalse(self):
		return False

	def test_createQualityObject_notComplete(self):
		native_isComplete=Assembly.isComplete
		Assembly.isComplete=self.dummy_returnFalse.im_func
		expected="The step is not complete yet"

		actual=""
		try:
			self.obj.createQualityObject()
		except Exception as e:
			actual=str(e)
		
		Assembly.isComplete=native_isComplete

		self.assertEqual(expected, actual)
	def test_createQualityObject_complete(self):
		self.assertEqual(1,2)
	def test_getQualityCount(self):
		self.assertEqual(1,2)
	def test_getQualityLength(self):
		self.assertEqual(1,2)

	def dummy_getLargeMemory(self):
		return -1
	def test_get_mem(self):
		Mock.getLargeMemory=tAssembly.dummy_getLargeMemory.im_func
		self.workspace.resources=Mock()

		self.assertEqual(self.dummy_getLargeMemory(), self.obj.getMem())

		del Mock.getLargeMemory
		del self.workspace.resources

	def dummy_getMediumTime(self):
		return -1
	def test_get_time(self):
		Mock.getMediumTime=tAssembly.dummy_getMediumTime.im_func
		self.workspace.resources=Mock()

		self.assertEqual(self.dummy_getMediumTime(), self.obj.getTime())

		del Mock.getMediumTime
		del self.workspace.resources

	def test_get_threads(self):
		self.assertEqual(1, self.obj.getThreads())

class tInput(unittest.TestCase):
	workspace=Mock(work_dir="work_dir", input_file="input_file")
	def setUp(self):
		self.obj=Input(self.workspace)
	def test_init_default(self):
		expected=[self.workspace, None]
		self.assertEqual(expected, [self.obj.workspace, self.obj.quality])

	def test_hash(self):
		expected=hash((self.workspace.input_file, self.workspace.work_dir, "Input"))
		self.assertEqual(expected, self.obj.__hash__())

	def test_str(self):
		self.assertEqual(self.workspace.input_file, str(self.obj))

	def test_writeCode(self):
		self.assertEqual([], self.obj.writeCode())

	def test_getStepDir(self):
		self.assertEqual(self.workspace.input_file, self.obj.getStepDir())

	def test_getOutputFile(self):
		self.assertEqual(self.workspace.input_file, self.obj.getOutputFile())

	def test_getOutputFileExtension(self):
		self.assertEqual("bnx", self.obj.getOutputFileExtension())

	def test_autoGeneratePrereqs(self):
		expected=self.obj.__dict__

		self.obj.autoGeneratePrereqs()

		self.assertEqual(expected, self.obj.__dict__)
	def test_getPrereq(self):
		self.assertEqual(None, self.obj.getPrereq())

	def test_isComplete_isComplete(self):
		expected=True
		with open(self.workspace.input_file, "w"):

			actual=self.obj.isComplete()

		os.remove(self.workspace.input_file)
		self.assertEqual(expected, actual)

	def test_isComplete_isNotComplete(self):
		expected=False

		actual=self.obj.isComplete()

		self.assertEqual(expected, actual)

	def test_getBnxFile_doesExist(self):
		expected="expected"
		actual="actual"
		with open(self.workspace.input_file, "w"):
			expected=BnxFile(self.workspace.input_file)
			actual=self.obj.getBnxFile()
		os.remove(self.workspace.input_file)

		self.assertEqual(expected, actual)
	def test_getBnxFile_doesNotExist(self):
		with self.assertRaises(IOError):
			self.obj.getBnxFile()

	def dummy_getBnxFile(self):
		return dummy_BnxFile()
	def dummy_saveQualityObjectToFile(self):
		self.savedQualityObjectToFile=True
	def test_createQualityObject(self):
		native_getBnxFile=Input.getBnxFile
		Input.getBnxFile=self.dummy_getBnxFile.im_func
		native_saveQualityObjectToFile=Input.saveQualityObjectToFile
		Input.saveQualityObjectToFile=self.dummy_saveQualityObjectToFile.im_func

		expected_count=0
		expected_quantity=0.0
		expected_labels=0
		for item in dummy_BnxFile().parse("bnx"):
			expected_count+=1
			expected_quantity+=item.length
			expected_labels+=item.num_labels

		expected=[expected_count, expected_quantity, expected_labels, True]

		self.obj.createQualityObject()
		actual=[self.obj.quality.count, self.obj.quality.quantity, self.obj.quality.labels, self.obj.savedQualityObjectToFile]

		Input.getBnxFile=native_getBnxFile
		Input.saveQualityObjectToFile=native_saveQualityObjectToFile

		self.assertEqual(expected, actual)

	def dummy_loadQuality_count(self):
		return 1
	def dummy_loadQuality_quantity(self):
		return 1
	def dummy_loadQuality_labels(self):
		return 1
	def dummy_loadQuality_density(self):
		return 1
	def dummy_loadQuality_averageLength(self):
		return 1
	def test_loadQualityReportItems(self):
		native_loadQuality_count=Input.loadQuality_count
		Input.loadQuality_count=self.dummy_loadQuality_count.im_func
		native_loadQuality_quantity=Input.loadQuality_quantity
		Input.loadQuality_quantity=self.dummy_loadQuality_quantity.im_func
		native_loadQuality_labels=Input.loadQuality_labels
		Input.loadQuality_labels=self.dummy_loadQuality_labels.im_func
		native_loadQuality_density=Input.loadQuality_density
		Input.loadQuality_density=self.dummy_loadQuality_density.im_func
		native_loadQuality_averageLength=Input.loadQuality_averageLength
		Input.loadQuality_averageLength=self.dummy_loadQuality_averageLength.im_func
		expected=OrderedDict()
		expected["File: " + self.obj.getOutputFile()]=3
		expected["Molecule count: " + str(self.dummy_loadQuality_count())]=1
		expected["Total quantity: " + str(self.dummy_loadQuality_quantity())]=1
		expected["Total labels: " + str(self.dummy_loadQuality_labels())]=1
		expected["Average label density: " + str(self.dummy_loadQuality_density())]=2
		expected["Average length: " + str(self.dummy_loadQuality_averageLength())]=2
		actual=self.obj.loadQualityReportItems()
		
		Input.loadQuality_count=native_loadQuality_count
		Input.loadQuality_quantity=native_loadQuality_quantity
		Input.loadQuality_labels=native_loadQuality_labels
		Input.loadQuality_density=native_loadQuality_density
		Input.loadQuality_averageLength=native_loadQuality_averageLength

		self.assertEqual(expected, actual)

	def dummy_createQualityObject(self):
		self.quality=Mock(createCalled=True, count=1, quantity=2, labels=3, density=4, average=5)

	def test_loadQuality_count_noneQuantity(self):
		native_createQualityObject=Input.createQualityObject
		Input.createQualityObject=self.dummy_createQualityObject.im_func

		self.dummy_createQualityObject()
		expected=[self.quality, self.quality.count]
		del self.quality

		count=self.obj.loadQuality_count()

		Input.createQualityObject=native_createQualityObject
		actual=[self.obj.quality,count]

		self.assertEqual(expected, actual)
	def test_loadQuality_count_someQuantity(self):
		quality=Mock(count=1)
		self.obj.quality=quality
		expected=[quality, quality.count]

		count=self.obj.loadQuality_count()

		self.assertEqual(expected, [self.obj.quality, count])

	def test_loadQuality_quantity_noneQuality(self):
		native_createQualityObject=Input.createQualityObject
		Input.createQualityObject=self.dummy_createQualityObject.im_func

		self.dummy_createQualityObject()
		expected=[self.quality, self.quality.quantity]
		del self.quality

		quantity=self.obj.loadQuality_quantity()

		Input.createQualityObject=native_createQualityObject
		actual=[self.obj.quality,quantity]

		self.assertEqual(expected, actual)
	def test_loadQuality_quantity_someQuality(self):
		quality=Mock(quantity=1)
		self.obj.quality=quality
		expected=[quality, quality.quantity]

		quantity=self.obj.loadQuality_quantity()

		self.assertEqual(expected, [self.obj.quality, quantity])

	def test_loadQuality_labels_noneQuality(self):
		native_createQualityObject=Input.createQualityObject
		Input.createQualityObject=self.dummy_createQualityObject.im_func

		self.dummy_createQualityObject()
		expected=[self.quality, self.quality.labels]
		del self.quality

		labels=self.obj.loadQuality_labels()

		Input.createQualityObject=native_createQualityObject
		actual=[self.obj.quality,labels]

		self.assertEqual(expected, actual)
	def test_loadQuality_labels_someQuality(self):
		quality=Mock(labels=1)
		self.obj.quality=quality
		expected=[quality, quality.labels]

		labels=self.obj.loadQuality_labels()

		self.assertEqual(expected, [self.obj.quality, labels])

	def test_loadQuality_density_noneQuality(self):
		native_createQualityObject=Input.createQualityObject
		Input.createQualityObject=self.dummy_createQualityObject.im_func

		self.dummy_createQualityObject()
		expected=[self.quality, self.quality.density]
		del self.quality

		density=self.obj.loadQuality_density()

		Input.createQualityObject=native_createQualityObject
		actual=[self.obj.quality,density]

		self.assertEqual(expected, actual)
	def test_loadQuality_density_qualityWithoutDensity(self):
		self.obj.quality=Mock(labels=2, quantity=1.0)
		expected = 2 / 1.0

		self.assertEqual(expected, self.obj.loadQuality_density())
	def test_loadQuality_density_qualityWithDensity(self):
		self.obj.quality=Mock(labels=2, quantity=1.0, density=10)
		expected=10

		self.assertEqual(expected, self.obj.loadQuality_density())

	def test_loadQuality_averageLength_noneQuality(self):
		native_createQualityObject=Input.createQualityObject
		Input.createQualityObject=self.dummy_createQualityObject.im_func

		self.dummy_createQualityObject()
		expected=[self.quality, self.quality.average]
		del self.quality

		average=self.obj.loadQuality_averageLength()

		Input.createQualityObject=native_createQualityObject
		actual=[self.obj.quality,average]

		self.assertEqual(expected, actual)
	def test_loadQuality_averageLength_qualityWithoutDensity(self):
		self.obj.quality=Mock(count=2, quantity=4.0)
		expected = 4.0 / 2

		self.assertEqual(expected, self.obj.loadQuality_averageLength())
	def test_loadQuality_averageLength_qualityWithDensity(self):
		self.obj.quality=Mock(count=2, quantity=4.0, average=10)
		expected=10

		self.assertEqual(expected, self.obj.loadQuality_averageLength())

	def test_getMem(self):
		self.assertEqual(-1, self.obj.getMem())
	def test_getTime(self):
		self.assertEqual(-1, self.obj.getTime())
	def test_getThreads(self):
		self.assertEqual(-1, self.obj.getThreads())

class dummy_BnxFile(object):
	def parse(self, formt):
		return [ Mock(length=100.0, num_labels=13),
			Mock(length=200.0, num_labels=26),
			Mock(length=300.0, num_labels=39) ]

class tRefineA(unittest.TestCase):
	workspace=Mock(work_dir="work_dir", input_file="input_file")
	vital_parameters=Mock(fp=1.5, fn=.150, pval=1e-5, min_molecule_len=100, min_molecule_sites=6)
	def setUp(self):
		native_autoGeneratePrereqs=RefineA.autoGeneratePrereqs
		RefineA.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func

		self.obj=RefineA(self.workspace, copy(self.vital_parameters))
		RefineA.autoGeneratePrereqs=native_autoGeneratePrereqs
	def dummy_getResources(self):
		return -1
	def dummy_autoGeneratePrereqs(self):
		self.autoGeneratePrereqsCalled=True
	def dummy_getStepDir(self):
		return "step_dir"
	def dummy_getOutputFileExtension(self):
		return "ext"
	def dummy_getOutputFile(self):
		return "output_file.ext"
	def test_constructor_default(self):
		expected=Mock(
			workspace=self.workspace,
			vital_parameters=self.vital_parameters,
			quality=None,
			sd=0.2,
			sf=0.2,
			sr=0.03,
			res=3.3,
			usecolor=1,
			use_multi_mode=True,
			consensus_end_coverage=0.99,
			bias_for_low_likelihood_ratio=1e2,
			refinement_length_accuracy="",
			largest_query_map_interval=4,
			largest_reference_map_interval=6,
			outlier_pval=1e-5,
			end_outlier_prior_probability=0.00001,
			contigs_format=1,
			overwrite_output=True,
			output_prefix="refineA",
			send_output_to_file=True,
			send_errors_to_file=True,
			total_job_count=1,
			autoGeneratePrereqsCalled=True)

		self.assertEqual(expected, self.obj)

	def test_writeCode(self):
		self.workspace.binaries={"bng_assembler": "Assembler"}
		native_getStepDir=RefineA.getStepDir
		RefineA.getStepDir=self.dummy_getStepDir.im_func
		native_getThreads=RefineA.getThreads
		RefineA.getThreads=self.dummy_getResources.im_func
		Mock.getOutputFile=self.dummy_getOutputFile.im_func
		self.obj.sort=Mock()
		self.obj.assembly=Mock()
		self.obj.molecule_stats=Mock()
		self.obj.group_manifest=Mock()

		expected=["cd " + self.workspace.work_dir + "\n"
 +
			"mkdir " + self.dummy_getStepDir() + "\n" +
			"cd " + self.dummy_getStepDir() + "\n" +
			"pwd\n" +
			"let contig_num=0\n" +
			"while read line\n" +
			"do\n" +
			"  if [[ $line == \"#\"* ]]; then continue; fi\n" +
			"  let contig_num+=1\n" +
			"  group_start=`echo $line | awk '{print $1}'`\n" +
			"  group_end=`echo $line | awk '{print $NF}'`\n" +
			"    Assembler -i ../" + self.dummy_getOutputFile() + " -contigs ../" + self.dummy_getOutputFile() + " $group_start $group_end -maxthreads -1 -T " + str(self.vital_parameters.pval) + " -usecolor 1 -extend 1 -refine 2 -MultiMode  -EndTrim 0.99 -LRbias 100.0 -Mprobeval  -deltaX 4 -deltaY 6 -outlier 1e-05 -endoutlier 1e-05 -contigs_format 1 -force  -FP " + str(self.vital_parameters.fp) + " -FN " + str(self.vital_parameters.fn) + " -sd 0.2 -sf 0.2 -sr 0.03 -res 3.3 -o refineA -stdout  -stderr  -XmapStatRead ../" + self.dummy_getOutputFile() + "\n" +
			"done < ../" + self.dummy_getOutputFile()]

		actual=self.obj.writeCode()
		
		del self.workspace.binaries
		RefineA.getStepDir=native_getStepDir
		RefineA.getThreads=native_getThreads
		del Mock.getOutputFile
		
		self.assertEqual(expected, actual)
	def test_getStepDir(self):
		Mock.getStepDir=self.dummy_getStepDir.im_func
		self.obj.inpt=Mock()
		expected="refineA_" + self.dummy_getStepDir() + "_fp" + str(self.vital_parameters.fp) + "_fn" + str(self.vital_parameters.fn) + "_pval" + str(self.vital_parameters.pval) + "_minlen" + str(self.vital_parameters.min_molecule_len) + "_minsites" + str(self.vital_parameters.min_molecule_sites)

		actual=self.obj.getStepDir()

		del Mock.getStepDir

		self.assertEqual(expected, actual)
	def test_getOutputFile(self):
		native_getStepDir=RefineA.getStepDir
		RefineA.getStepDir=self.dummy_getStepDir.im_func
		native_getOutputFileExtension=RefineA.getOutputFileExtension
		RefineA.getOutputFileExtension=self.dummy_getOutputFileExtension.im_func
		self.obj.output_prefix="output_prefix"
		expected=self.dummy_getStepDir() + "/" + self.obj.output_prefix + "." + self.dummy_getOutputFileExtension()

		actual=self.obj.getOutputFile()

		RefineA.getStepDir=native_getStepDir
		RefineA.getOutputFileExtension=native_getOutputFileExtension

		self.assertEqual(expected, actual)

	def test_getOutputFileExtension(self):
		self.assertEqual("contigs", self.obj.getOutputFileExtension())
	def test_autoGeneratePrereqs(self):
		native_getTime_split=Split.getTime
		Split.getTime=self.dummy_getResources.im_func
		native_getTime_pairwise=PairwiseAlignment.getTime
		PairwiseAlignment.getTime=self.dummy_getResources.im_func

		self.vital_parameters.blocks=1
		self.obj.vital_parameters.blocks=1
		self.obj.inpt=Input(self.workspace)
		sort=Sort(self.workspace, copy(self.vital_parameters))
		self.obj.sort=sort
		self.obj.molecule_stats=sort.getMoleculeStats()
		split=Split(self.workspace, copy(self.vital_parameters))
		self.obj.split=split
		self.obj.split_summary=Summarize(self.workspace, split)
		pairwise_alignment=PairwiseAlignment(self.workspace, copy(self.vital_parameters))
		self.obj.pairwise_alignment=pairwise_alignment
		self.obj.pairwise_summary=Summarize(self.workspace, pairwise_alignment)
		assembly=Assembly(self.workspace, copy(self.vital_parameters))
		self.obj.assembly=assembly
		self.obj.assembly_summary=Summarize(self.workspace, assembly)
		self.obj.merge_assembly=Merge(self.workspace, assembly)
		self.obj.group_manifest=GroupManifest(self.workspace, assembly)

		actual=RefineA(self.workspace, copy(self.vital_parameters))
		actual.autoGeneratePrereqs()
		actual.autoGeneratePrereqsCalled=True

		Split.getTime=native_getTime_split
		PairwiseAlignment.getTime=native_getTime_pairwise
		del self.vital_parameters.blocks

		self.assertEqual(self.obj.__dict__, actual.__dict__)

	def test_getPrereq(self):
		expected=Mock()
		self.obj.group_manifest=expected

		actual=self.obj.getPrereq()

		self.assertEqual(expected, actual)
	def test_getMem(self):
		Mock.getMediumMemory=self.dummy_getResources.im_func
		self.obj.workspace.resources=Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getMem()

		del Mock.getMediumMemory
		del self.obj.workspace.resources

		self.assertEqual(expected, actual)
	def test_getTime(self):
		Mock.getLargeTime=self.dummy_getResources.im_func
		self.obj.workspace.resources=Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getTime()

		del Mock.getLargeTime
		del self.obj.workspace.resources

		self.assertEqual(expected, actual)
	def test_getThreads(self):
		Mock.getMediumThreads=self.dummy_getResources.im_func
		self.obj.workspace.resources=Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getThreads()

		del Mock.getMediumThreads
		del self.obj.workspace.resources

		self.assertEqual(expected, actual)

class tGroupManifest(unittest.TestCase):
	workspace=Mock(work_dir="work_dir", input_file="input_file")
	assembly=Mock(output_prefix="output_prefix", vital_parameters=Mock(fp=1.5, fn=.150, pval=1e-5, min_molecule_len=100, min_molecule_sites=6), quality=None)
	native_autoGen=GroupManifest.autoGeneratePrereqs
	def setUp(self):
		GroupManifest.autoGeneratePrereqs=self.dummy_autoGen.im_func

		self.obj=GroupManifest(self.workspace, self.assembly)

		GroupManifest.autoGeneratePrereqs=self.native_autoGen
	def dummy_autoGen(self):
		self.autoGenCalled=True
	def dummy_getResources(self):
		return -1
	def dummy_getStepDir(self):
		return "step_dir"
	def dummy_getOutputFile(self):
		return "output_file.ext"
	def dummy_makeWeightStatsFile(self):
		self.makeWeightStatsFileCalled=True
		with open("weight_stats.txt", "w"):
			pass
	def dummy__makeGroupManifestFile(self, dummy1, dummy2):
		self._makeGroupManifestFileCalled=True


	def test_constructor_default(self):
		expected=Mock(
			workspace=self.workspace,
			assembly=self.assembly,
			quality=None,
			autoGenCalled=True)

		self.assertEqual(expected, self.obj)

	def test_writeCode(self):
		native_getStepDir=GroupManifest.getStepDir
		GroupManifest.getStepDir=self.dummy_getStepDir.im_func

		expected="cd " + self.workspace.work_dir + "\n"
		expected+="mkdir " + self.dummy_getStepDir() + "\n"
		expected+="cd " + self.dummy_getStepDir() + "\n"
		expected+="pwd\n"
		expected+="python -c 'from Utils.Workspace import Workspace;"
		expected+="from Operations.BioNano.Assemble.VitalParameters import VitalParameters;"
		expected+="from Operations.BioNano.Assemble.Assembly import GenericAssembly;"
		expected+="from Operations.BioNano.Assemble.GroupManifest import GroupManifest;"
		expected+="ws=Workspace(\"" + self.workspace.work_dir + "\", \"" + self.workspace.input_file + "\");"
		expected+="vp=VitalParameters(" + str(self.assembly.vital_parameters.fp) + ", " + str(self.assembly.vital_parameters.fn) + ", " + str(self.assembly.vital_parameters.pval) + ", " + str(self.assembly.vital_parameters.min_molecule_len) + ", " + str(self.assembly.vital_parameters.min_molecule_sites) + ");"
		expected+="gm=GroupManifest(ws, GenericAssembly.createAssembly(ws, vp, \"\"));"
		expected+="gm.makeGroupManifestFile()'"

		actual=self.obj.writeCode()

		GroupManifest.getStepDir=native_getStepDir
		
		self.assertEqual([expected], actual)

	def test_makeGroupManifestFile_weightStatsDoesNotExist(self):
		self.obj.makeWeightStatsFileCalled=False
		native_getOutputFile=GroupManifest.getOutputFile
		GroupManifest.getOutputFile=self.dummy_getOutputFile.im_func
		native_makeWeightStatsFile=GroupManifest.makeWeightStatsFile
		GroupManifest.makeWeightStatsFile=self.dummy_makeWeightStatsFile.im_func
		native__makeGroupManifestFile=GroupManifest._makeGroupManifestFile
		GroupManifest._makeGroupManifestFile=self.dummy__makeGroupManifestFile.im_func

		expected_makeWeightStatsFileCalled=True
		expected__makeGroupManifestFileCalled=True
		expected_weightStatsFileExists=True
		expected_outputFileExists=True
		expected_completeStatusExists=True
		expected=[expected_makeWeightStatsFileCalled, expected__makeGroupManifestFileCalled, expected_weightStatsFileExists, expected_outputFileExists, expected_completeStatusExists]

		self.obj.makeGroupManifestFile()

		GroupManifest.getOutputFile=native_getOutputFile
		GroupManifest.makeWeightStatsFile=native_makeWeightStatsFile
		GroupManifest._makeGroupManifestFile=native__makeGroupManifestFile

		actual_weightStatsFileExists=True
		actual_outputFileExists=True
		actual_completeStatusExists=True

		try:
			os.remove("weight_stats.txt")
		except OSError:
			actual_weightStatsFileExists=False
		try:
			os.remove("../" + self.dummy_getOutputFile())
		except OSError:
			acutal_outputFileExists=False
		try: 
			os.remove("Complete.status")
		except OSError:
			actual_completeStatusExists=False
		actual=[self.obj.makeWeightStatsFileCalled, self.obj._makeGroupManifestFileCalled, actual_weightStatsFileExists, actual_outputFileExists, actual_completeStatusExists]

		self.assertEqual(expected, actual)

	def test_makeGroupManifestFile_weightStatsDoesExist(self):
		self.obj.makeWeightStatsFileCalled=False
		native_getOutputFile=GroupManifest.getOutputFile
		GroupManifest.getOutputFile=self.dummy_getOutputFile.im_func
		native_makeWeightStatsFile=GroupManifest.makeWeightStatsFile
		GroupManifest.makeWeightStatsFile=self.dummy_makeWeightStatsFile.im_func
		native__makeGroupManifestFile=GroupManifest._makeGroupManifestFile
		GroupManifest._makeGroupManifestFile=self.dummy__makeGroupManifestFile.im_func

		expected_makeWeightStatsFileCalled=False
		expected__makeGroupManifestFileCalled=True
		expected_outputFileExists=True
		expected_completeStatusExists=True
		expected=[expected_makeWeightStatsFileCalled, expected__makeGroupManifestFileCalled, expected_outputFileExists, expected_completeStatusExists]

		with open("weight_stats.txt", "w"):
			self.obj.makeGroupManifestFile()

		GroupManifest.getOutputFile=native_getOutputFile
		GroupManifest.makeWeightStatsFile=native_makeWeightStatsFile
		GroupManifest._makeGroupManifestFile=native__makeGroupManifestFile

		actual_outputFileExists=True
		actual_completeStatusExists=True

		os.remove("weight_stats.txt")
		try:
			os.remove("../" + self.dummy_getOutputFile())
		except OSError:
			acutal_outputFileExists=False
		try: 
			os.remove("Complete.status")
		except OSError:
			actual_completeStatusExists=False
		actual=[self.obj.makeWeightStatsFileCalled, self.obj._makeGroupManifestFileCalled, actual_outputFileExists, actual_completeStatusExists]

		self.assertEqual(expected, actual)

	def test__makeGroupManifestFile(self):
		self.assertEqual(1,2)

	def test_makeWeightStatsFile(self):
		self.assertEqual(1,2)

	def test_getStepDir(self):
		Mock.getStepDir=self.dummy_getStepDir.im_func
		self.obj.merge_assembly=Mock()
		expected=self.dummy_getStepDir()

		actual=self.obj.getStepDir()

		del Mock.getStepDir

		self.assertEqual(expected, actual)
	def test_getOutputFile(self):
		native_getStepDir=GroupManifest.getStepDir
		GroupManifest.getStepDir=self.dummy_getStepDir.im_func
		Mock.getStepDir=self.dummy_getStepDir.im_func
		expected=self.dummy_getStepDir() + "/" + self.assembly.output_prefix + ".group_manifest"

		actual=self.obj.getOutputFile()

		GroupManifest.getStepDir=native_getStepDir
		del Mock.getStepDir
		self.assertEqual(expected, actual)

	def test_getOutputFileExtension(self):
		self.assertEqual("group_manifest", self.obj.getOutputFileExtension())
	def test_autoGeneratePrereqs(self):
		native_Summarize_autoGen=Summarize.autoGeneratePrereqs
		Summarize.autoGeneratePrereqs=self.dummy_autoGen.im_func
		native_Merge_autoGen=Merge.autoGeneratePrereqs
		Merge.autoGeneratePrereqs=self.dummy_autoGen.im_func
		self.obj.assembly_summary=Summarize(self.workspace, self.assembly)
		self.obj.merge_assembly=Merge(self.workspace, self.assembly)

		actual=GroupManifest(self.workspace, self.assembly)
		actual.autoGenCalled=True

		Summarize.autoGeneratePrereqs=native_Summarize_autoGen
		Merge.autoGeneratePrereqs=native_Merge_autoGen
		
		self.assertEqual(self.obj.__dict__, actual.__dict__)
		
	def test_getPrereq(self):
		expected=Mock()
		self.obj.merge_assembly=expected

		self.assertEqual(expected, self.obj.getPrereq())

	def test_getMem(self):
		Mock.getSmallMemory=self.dummy_getResources.im_func
		self.obj.workspace.resources=Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getMem()

		del self.obj.workspace.resources
		del Mock.getSmallMemory

		self.assertEqual(expected, actual)
	def test_getTime(self):
		Mock.getSmallTime=self.dummy_getResources.im_func
		self.obj.workspace.resources=Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getTime()

		del self.obj.workspace.resources
		del Mock.getSmallTime

		self.assertEqual(expected, actual)
	def test_getThreads(self):
		self.assertEqual(1, self.obj.getThreads())

class tRefineB0(unittest.TestCase):
	workspace=Mock(work_dir="work_dir", input_file="input_file")
	vital_parameters=Mock(fp=1.5, fn=.150, pval=1e-5, min_molecule_len=100, min_molecule_sites=6)

	def setUp(self):
		native_autoGeneratePrereqs=RefineB0.autoGeneratePrereqs
		RefineB0.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func

		self.obj=RefineB0(self.workspace, self.vital_parameters)

		RefineB0.autoGeneratePrereqs=native_autoGeneratePrereqs

	def dummy_autoGeneratePrereqs(self):
		self.autoGeneratePrereqsCalled=True
	def dummy_getResources(self):
		return -1
	def dummy_getString(self, block=None):
		return "string"

	def test_init_default(self):
		expected={"autoGeneratePrereqsCalled": True,
			"workspace": self.workspace,
			"vital_parameters": self.vital_parameters,
			"quality": None,
			"output_prefix": "refineB0",
			"color": 1,
			"aligned_site_threshold": 5,
			"max_coverage": 100,
			"enable_multi_mode": True,
			"internal_split_ratio": 0.20,
			"internal_trimmed_coverage_ratio": 0.35,
			"cnt_file": "refineB0_max_id",
			"min_contig_len": 100.0,
			"allow_no_splits": True,
			"allow_infinite_splits": False,
			"min_end_coverage": 6.99,
			"scale_bias_wt": 0,
			"min_likelihood_ratio": 1e2,
			"max_query_alignment": 4,
			"max_reference_alignment": 6,
			"max_repeat_shift": 2,
			"repeat_pval_ratio": 0.01,
			"repeat_log_pval_ratio": 0.7,
			"repeat_min_shift_ratio": 0.6,
			"min_gap_flanking_sites": 2,
			"output_trimmed_coverage": True,
			"normalize_trimmed_coverage": True,
			"min_gap_flanking_len": 55,
			"last_non_chimeric_site_after_gap": 2,
			"split_molecules_with_outliers": True,
			"outlier_pvals_per_true_positive": 1e-5,
			"end_outlier_prior_probability": 1e-4,
			"pval_after_refinement": 1,
			"faster_refinement_resolution": "",
			"count_splits_with_largest_ids": True,
			"contig_split_version": "",
			"reduced_contig_resolution_divided_by_two": 2.0,
			"overwrite_output": True,
			"hash_window": 5,
			"hash_min_sites": 3,
			"hash_sd_max": 2.4,
			"hash_sd_rms": 1.5,
			"hash_relative_error": 0.05,
			"hash_offset_kb": 5.0,
			"hash_max_insert_errors": 1,
			"hash_max_probe_errors": 1,
			"hash_max_unresolved_sites": 1,
			"hash_file": "",
			"hash_threshold": "",
			"hashdelta": 10,
			"reduced_molecule_resolution": 1.2,
			"insert_threads": 4,
			"skip_alignment_statistic_computation": True,
			"sd": 0.2,
			"sf": 0.2,
			"sr": 0.03,
			"res": 3.3,
			"regex_acceptible_output_file": ".*.bnx",
			"write_output_to_file": True,
			"write_errors_to_file": True,
			"max_job_count": 2
			}

		self.maxDiff=None
		self.assertEqual(expected, self.obj.__dict__)
	def getCode(self, block):
		return "bng_ref_aligner -i string -o refineB0 -maxthreads -1 -ref string -T 1e-05 -usecolor 1 -A 5 -extend 1 -MaxCov 100 -MultiMode  -contigsplit 0.2 0.35 refineB0_max_id -MinSplitLen 100.0 -nosplit 2 -EndTrim 6.99 -biaswt 0 -LRbias 100.0 -deltaX 4 -deltaY 6 -RepeatMask 2 0.01 -RepeatRec 0.7 0.6 -CovTrim 2 -ReplaceCov  -TrimNorm  -CovTrimLen 55 -TrimNormChim 2 -TrimOutlier  -outlier 1e-05 -endoutlier 0.0001 -endoutlierFinal 1 -Mprobeval  -splitcnt  -splitrev  -rres 2.0 -f  -refine 0 -hashgen 5 3 2.4 1.5 0.05 5.0 1 1 1 -hash   -hashdelta 10 -mres 1.2 -insertThreasds 4 -nostat  -maxmem -1 -FP 1.5 -FN 0.15 -sd 0.2 -sf 0.2 -sr 0.03 -res 3.3 -grouped ../string -mapped refineB0_id" + str(block) + "_mapped -output-filter .*.bnx -id " + str(block) + " -stdout  -stderr  -XmapStatRead ../string -minlen 100 -minsites 6\n"
	def test_writeCode_lessThan2BlocksOdd(self):
		self.obj.split=Mock(vital_parameters=Mock(blocks=1))
		native_getStepDir=RefineB0.getStepDir
		RefineB0.getStepDir=self.dummy_getString.im_func
		native_getThreads=RefineB0.getThreads
		RefineB0.getThreads=self.dummy_getResources.im_func
		self.obj.merge_refineA=Mock()
		Mock.getOutputFile=self.dummy_getString.im_func
		native_getMem=RefineB0.getMem
		RefineB0.getMem=self.dummy_getResources.im_func
		self.obj.group_manifest=Mock()
		self.obj.molecule_stats=Mock()
		self.workspace.binaries={"bng_ref_aligner": "bng_ref_aligner"}
		
		header="\n".join(["cd " + self.workspace.work_dir,
			"mkdir -p " + self.dummy_getString(),
			"cd " + self.dummy_getString(),
			"pwd\n"])
		code=self.getCode(1)
		expected=[header+code]

		actual=self.obj.writeCode()

		RefineB0.getStepDir=native_getStepDir
		RefineB0.getThreads=native_getThreads
		del Mock.getOutputFile
		RefineB0.getMem=native_getMem
		del self.workspace.binaries

		self.assertEqual(expected,actual)
	def test_writeCode_moreThan2BlocksEven(self):
		self.obj.split=Mock(vital_parameters=Mock(blocks=4))
		native_getStepDir=RefineB0.getStepDir
		RefineB0.getStepDir=self.dummy_getString.im_func
		native_getThreads=RefineB0.getThreads
		RefineB0.getThreads=self.dummy_getResources.im_func
		self.obj.merge_refineA=Mock()
		Mock.getOutputFile=self.dummy_getString.im_func
		native_getMem=RefineB0.getMem
		RefineB0.getMem=self.dummy_getResources.im_func
		self.obj.group_manifest=Mock()
		self.obj.molecule_stats=Mock()
		self.workspace.binaries={"bng_ref_aligner": "bng_ref_aligner"}
		
		header="\n".join(["cd " + self.workspace.work_dir,
			"mkdir -p " + self.dummy_getString(),
			"cd " + self.dummy_getString(),
			"pwd\n"])
		code=self.getCode(1)
		expected=["".join([header,self.getCode(1), "", self.getCode(2)]),
			"".join([header,self.getCode(3), "", self.getCode(4)])]

		actual=self.obj.writeCode()

		RefineB0.getStepDir=native_getStepDir
		RefineB0.getThreads=native_getThreads
		del Mock.getOutputFile
		RefineB0.getMem=native_getMem
		del self.workspace.binaries

		self.assertEqual(expected,actual)
	def test_getStepDir(self):
		expected="_".join(["refineB0", "fp"+str(self.vital_parameters.fp), "fn"+str(self.vital_parameters.fn), "pval"+str(self.vital_parameters.pval), "minlen"+str(self.vital_parameters.min_molecule_len), "minsites"+str(self.vital_parameters.min_molecule_sites)])

		actual=self.obj.getStepDir()

		self.assertEqual(expected, actual)
	def test_getOutputFileExtension(self):
		self.assertEqual("bnx", self.obj.getOutputFileExtension())

	def test_autoGeneratePrereqs(self):
		Mock.getSmallTime=self.dummy_getResources.im_func
		Mock.getLargeTime=self.dummy_getResources.im_func
		self.workspace.resources=Mock()
		self.obj.workspace.resources=Mock()
		self.obj.vital_parameters.blocks=1

		self.obj.inpt=Input(self.workspace)
		sort=Sort(self.workspace, copy(self.vital_parameters))
		self.obj.sort=sort
		self.obj.molecule_stats=sort.getMoleculeStats()
		split=Split(self.workspace, copy(self.vital_parameters))
		self.obj.split=split
		self.obj.split_summary=Summarize(self.workspace, split)
		pairwise_alignment=PairwiseAlignment(self.workspace, copy(self.vital_parameters))
		self.obj.pairwise_alignment=pairwise_alignment
		self.obj.pairwise_summary=Summarize(self.workspace, pairwise_alignment)
		assembly=Assembly(self.workspace, copy(self.vital_parameters))
		self.obj.assembly=assembly
		self.obj.assembly_summary=Summarize(self.workspace, assembly)
		self.obj.merge_assembly=Merge(self.workspace, assembly)
		refineA=RefineA(self.workspace, copy(self.vital_parameters))
		self.obj.refineA=refineA
		self.obj.refineA_summary=Summarize(self.workspace, refineA)
		self.obj.merge_refineA=Merge(self.workspace, refineA)

		self.obj.autoGeneratePrereqs()
		actual=RefineB0(self.workspace, self.vital_parameters)
		actual.autoGeneratePrereqsCalled=True

		del self.workspace.resources
		del self.vital_parameters.blocks
		del Mock.getSmallTime
		del Mock.getLargeTime

		self.assertEqual(self.obj, actual)
	
	def test_getPrereq(self):
		expected=Mock(name="group_manifest")
		self.obj.group_manifest=expected

		actual=self.obj.getPrereq()

		self.assertEqual(expected, actual)

	def test_getMem(self):
		Mock.getMediumMemory=self.dummy_getResources.im_func
		self.obj.workspace.resources=Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getMem()

		del Mock.getMediumMemory

		self.assertEqual(expected, actual)
	def test_getTime(self):
		Mock.getLargeTime=self.dummy_getResources.im_func
		self.obj.workspace.resources=Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getTime()

		del Mock.getLargeTime

		self.assertEqual(expected, actual)
	def test_getThreads(self):
		Mock.getMediumThreads=self.dummy_getResources.im_func
		self.obj.workspace.resources=Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getThreads()

		del Mock.getMediumThreads

		self.assertEqual(expected, actual)

class tMerge(unittest.TestCase):
	workspace=Mock(work_dir="work_dir", input_file="input_file")
	assembly=Mock(quality=None, output_prefix="unrefined")
	native_autoGeneratePrereqs=Merge.autoGeneratePrereqs

	def dummy_autoGen(self):
		self.autoGenCalled=True
	def dummy_getStepDir(self):
		return "step_dir"
	def dummy_getOutputFile(self):
		return "output_file"
	def dummy_getOutputFileExtension(self):
		return "cmap"
	def setUp(self):
		Merge.autoGeneratePrereqs=self.dummy_autoGen.im_func
		self.obj=Merge(self.workspace, self.assembly)
		Merge.autoGeneratePrereqs=self.native_autoGeneratePrereqs

	def test_init(self):
		expected=[self.workspace, self.assembly, self.assembly.quality, True, "merge_of_unrefined", True, True, True]
		actual=[self.obj.workspace, self.obj.assembly, self.obj.assembly.quality, self.obj.autoGenCalled, self.obj.output_prefix, self.obj.overwrite_output, self.obj.write_output_to_file, self.obj.write_error_to_file]
		self.assertEqual(expected, actual)

	def test_writeCode(self):
		native_getStepDir=Merge.getStepDir
		Merge.getStepDir=self.dummy_getStepDir.im_func
		self.workspace.binaries={"bng_ref_aligner": "binary"}
		Mock.getOutputFile=self.dummy_getOutputFile.im_func
		self.obj.assembly_summary=Mock()

		expected=["cd " + self.workspace.work_dir + "\n" + "mkdir -p " + self.dummy_getStepDir() + "\n" + "cd " + self.dummy_getStepDir() + "\n" + "pwd\n" + "binary -if ../" + self.dummy_getOutputFile() + " -merge  -o " + self.obj.output_prefix + " -f  -stdout  -stderr \nresult=`tail -n 1 ../" + self.dummy_getStepDir() + "/" + self.obj.output_prefix + ".stdout`\nif [[ \"$result\" != \"END of output\" ]]; then exit 1; else touch Complete.status; fi\n"]
		actual=self.obj.writeCode()

		Merge.getStepDir=native_getStepDir
		del self.workspace.binaries
		del Mock.getOutputFile

		self.assertEqual(expected, actual)
			

	def test_getStepDir(self):
		Mock.getStepDir=self.dummy_getStepDir.im_func
		expected="merged_"+self.dummy_getStepDir()
		
		actual=self.obj.getStepDir()

		del Mock.getStepDir

		self.assertEqual(expected, actual)

	def test_getOutputFile(self):
		native_getStepDir=Merge.getStepDir
		Merge.getStepDir=self.dummy_getStepDir.im_func
		native_getOutputFileExtension=Merge.getOutputFileExtension
		Merge.getOutputFileExtension=self.dummy_getOutputFileExtension.im_func
		self.obj.output_prefix="output_prefix"

		expected=self.dummy_getStepDir() + "/output_prefix." + self.dummy_getOutputFileExtension()
		actual=self.obj.getOutputFile()

		Merge.getStepDir=native_getStepDir
		Merge.getOutputFileExtension=native_getOutputFileExtension

		self.assertEqual(expected, actual)
	def test_getOutputFileExtension(self):
		self.assertEqual("cmap", self.obj.getOutputFileExtension())
	def test_autoGeneratePrereqs(self):
		self.obj.autoGeneratePrereqs()
		expected=Summarize(self.workspace, self.assembly)

		self.assertEqual(expected, self.obj.assembly_summary)
	def test_getPrereq(self):
		expected=Mock()
		self.obj.assembly_summary=expected

		self.assertEqual(expected, self.obj.getPrereq())

	def dummy_getResources(self):
		return -1
	def test_getMem(self):
		Mock.getSmallMemory=self.dummy_getResources.im_func
		self.workspace.resources=Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getMem()

		del Mock.getSmallMemory
		del self.workspace.resources

		self.assertEqual(expected, actual)
	def test_getTime(self):
		Mock.getSmallTime=self.dummy_getResources.im_func
		self.workspace.resources=Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getTime()

		del Mock.getSmallTime
		del self.workspace.resources

		self.assertEqual(expected, actual)
	def test_getThreads(self):
		self.assertEqual(1, self.obj.getThreads())

class tSummarize(unittest.TestCase):
	step=Mock()
	workspace=Mock(work_dir="work_dir", input_file="input_file")
	vital_parameters=Mock(pval=1e-5, fp=1.5, fn=.015, min_molecule_len=100, min_molecule_sites=6, blocks=1)
	def dummy_autoGeneratePrereqs(self):
		self.autoGeneratePrereqsCalled=True
	def dummy_getString(self):
		return "string"
	def dummy_getNumber(self):
		return -1

	def setUp(self):
		native_autoGeneratePrereqs=Summarize.autoGeneratePrereqs
		Summarize.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func

		self.obj=Summarize(self.workspace, self.step)

		Summarize.autoGeneratePrereqs=native_autoGeneratePrereqs

	def test_init(self):
		expected=Mock(workspace=self.workspace, step=self.step, autoGeneratePrereqsCalled=True)

		self.assertEqual(expected, self.obj)
	def test_hash(self):
		self.obj.step.vital_parameters=self.vital_parameters
		expected=hash((self.workspace.input_file, self.workspace.work_dir, self.vital_parameters.pval, self.vital_parameters.fp, self.vital_parameters.fn, self.vital_parameters.min_molecule_len, self.vital_parameters.min_molecule_sites, "Summarize"))

		self.assertEqual(expected, self.obj.__hash__())

	def test_eq_none(self):
		other=None
		self.assertFalse(self.obj==other)
	def test_eq_diffClass(self):
		other=Mock(workspace=self.workspace, step=self.step)
		self.assertFalse(self.obj==other)
	def test_eq_areEqual(self):
		other=Summarize(self.workspace, self.step)
		self.assertTrue(self.obj==other)

	def test_writeCode_default(self):
		native_getOutputFile=Summarize.getOutputFile
		Summarize.getOutputFile=self.dummy_getString.im_func
		native_getStepDir=Summarize.getStepDir
		Summarize.getStepDir=self.dummy_getString.im_func
		Mock.getOutputFileExtension=self.dummy_getString.im_func
		total_job_count=-1
		self.obj.step.total_job_count=total_job_count

		expected="\n".join(["wd=`pwd`",
			"rm -f " + self.dummy_getString() + "",
			"let errors=0",
			"let total=0",
			"for stdout_file in " + self.dummy_getString() + "/*.stdout",
			"do",
			"  let total+=1",
			"  result=`tail -n 1 $stdout_file`",
			"  if [[ $result != \"END of output\" ]]; then let errors+=1",
			"  else",
			"    file=`echo $stdout_file | sed 's/\.stdout/\." + self.dummy_getString() + "/'`",
			"    echo $wd/$file >> " + self.dummy_getString() + ";",
			"  fi",
			"done",
			"if [ $total -lt " + str(total_job_count) + " ]; then let errors+=1; fi",
			"if [ $errors -ne 0 ]; then exit 1; else touch " + self.dummy_getString() + "/Complete.status; fi\n"])

		actual=self.obj.writeCode()

		Summarize.getOutputFile=native_getOutputFile
		Summarize.getStepDir=native_getStepDir
		del Mock.getOutputFileExtension

		self.maxDiff=None
		self.assertEqual([expected], actual)

	def test_writeCode_assembly(self):
		native_autoGen=Assembly.autoGeneratePrereqs
		Assembly.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func
		self.obj.step=Assembly(self.workspace, self.vital_parameters)
		native_getOutputFile=Summarize.getOutputFile
		Summarize.getOutputFile=self.dummy_getString.im_func
		native_getStepDir=Summarize.getStepDir
		Summarize.getStepDir=self.dummy_getString.im_func
		Mock.getOutputFileExtension=self.dummy_getString.im_func
		total_job_count=-1
		self.obj.step.total_job_count=total_job_count

		expected="\n".join(["wd=`pwd`",
			"rm -f " + self.dummy_getString() + "",
			"let errors=0",
			"let total=0",
			"for stdout_file in " + self.dummy_getString() + "/*.stdout",
			"do",
			"  let total+=1",
			"  result=`tail -n 1 $stdout_file`",
			"  if [[ $result != \"END of output\" ]]; then let errors+=1",
			"  fi",
			"done",
			"if [ $total -lt " + str(total_job_count) + " ]; then let errors+=1; fi",
			"if [ $errors -ne 0 ]; then exit 1; else touch " + self.dummy_getString() + "/Complete.status; fi",
			"ls " + self.dummy_getString() + "/*.cmap | while read file; do echo $wd/$file >> " + self.dummy_getString() + "; done;\n"])
		actual=self.obj.writeCode()

		Summarize.getOutputFile=native_getOutputFile
		Summarize.getStepDir=native_getStepDir
		del Mock.getOutputFileExtension
		Assembly.autoGeneratePrereqs=native_autoGen
		
		self.assertEqual([expected], actual)
	def test_writeCode_refineA(self):
		native_autoGen=RefineA.autoGeneratePrereqs
		RefineA.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func
		self.obj.step=RefineA(self.workspace, self.vital_parameters)
		native_getOutputFile=Summarize.getOutputFile
		Summarize.getOutputFile=self.dummy_getString.im_func
		native_getStepDir=Summarize.getStepDir
		Summarize.getStepDir=self.dummy_getString.im_func
		Mock.getOutputFileExtension=self.dummy_getString.im_func
		total_job_count=-1
		self.obj.step.total_job_count=total_job_count

		expected="\n".join(["wd=`pwd`",
			"rm -f " + self.dummy_getString() + "",
			"let errors=0",
			"let total=0",
			"for stdout_file in " + self.dummy_getString() + "/*.stdout",
			"do",
			"  let total+=1",
			"  result=`tail -n 1 $stdout_file`",
			"  if [[ $result != \"END of output\" ]]; then let errors+=1",
			"  fi",
			"done",
			"if [ $total -lt " + str(total_job_count) + " ]; then let errors+=1; fi",
			"if [ $errors -ne 0 ]; then exit 1; else touch " + self.dummy_getString() + "/Complete.status; fi",
			"ls " + self.dummy_getString() + "/*.cmap | while read file; do echo $wd/$file >> " + self.dummy_getString() + "; done;\n"])
		actual=self.obj.writeCode()

		Summarize.getOutputFile=native_getOutputFile
		Summarize.getStepDir=native_getStepDir
		del Mock.getOutputFileExtension
		RefineA.autoGeneratePrereqs=native_autoGen
		
		self.assertEqual([expected], actual)

	def test_getStepDir(self):
		Mock.getStepDir=self.dummy_getString.im_func

		expected=self.dummy_getString()
		actual=self.obj.getStepDir()

		del Mock.getStepDir

		self.assertEqual(expected, actual)

	def test_autoGeneratePrereqs(self):
		self.obj.autoGeneratePrereqs()

	def test_getPrereq(self):
		self.assertEqual(self.step, self.obj.getPrereq())

	def test_getOutputFile_split(self):
		native_getStepDir=Summarize.getStepDir
		Summarize.getStepDir=self.dummy_getString.im_func
		native_getOutputFileExtension=Summarize.getOutputFileExtension
		Summarize.getOutputFileExtension=self.dummy_getString.im_func
		native_autoGeneratePrereqs=Split.autoGeneratePrereqs
		Split.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func
		native_getTime=Split.getTime
		Split.getTime=self.dummy_getNumber.im_func
		self.obj.step=Split(self.workspace, self.vital_parameters)

		expected=self.dummy_getString() + "/split." + self.dummy_getString()
		actual=self.obj.getOutputFile()

		Summarize.getStepDir=native_getStepDir
		Summarize.getOutputFileExtension=native_getOutputFileExtension
		Split.autoGeneratePrereqs=native_autoGeneratePrereqs
		Split.getTime=native_getTime

		self.assertEqual(expected, actual)
		
	def test_getOutputFile_pairwise(self):
		native_getStepDir=Summarize.getStepDir
		Summarize.getStepDir=self.dummy_getString.im_func
		native_getOutputFileExtension=Summarize.getOutputFileExtension
		Summarize.getOutputFileExtension=self.dummy_getString.im_func
		native_split_autoGeneratePrereqs=Split.autoGeneratePrereqs
		Split.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func
		native_split_getTime=Split.getTime
		Split.getTime=self.dummy_getNumber.im_func
		native_pairwise_autoGeneratePrereqs=PairwiseAlignment.autoGeneratePrereqs
		PairwiseAlignment.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func
		native_pairwise_getTime=PairwiseAlignment.getTime
		PairwiseAlignment.getTime=self.dummy_getNumber.im_func
		self.obj.step=PairwiseAlignment(self.workspace, self.vital_parameters)

		expected=self.dummy_getString() + "/align." + self.dummy_getString()
		actual=self.obj.getOutputFile()

		Summarize.getStepDir=native_getStepDir
		Summarize.getOutputFileExtension=native_getOutputFileExtension
		Split.autoGeneratePrereqs=native_split_autoGeneratePrereqs
		Split.getTime=native_split_getTime
		PairwiseAlignment.autoGeneratePrereqs=native_pairwise_autoGeneratePrereqs
		PairwiseAlignment.getTime=native_pairwise_getTime

		self.assertEqual(expected, actual)

	def test_getOutputFile_assembly(self):
		native_getStepDir=Summarize.getStepDir
		Summarize.getStepDir=self.dummy_getString.im_func
		native_getOutputFileExtension=Summarize.getOutputFileExtension
		Summarize.getOutputFileExtension=self.dummy_getString.im_func
		native_autoGeneratePrereqs=Assembly.autoGeneratePrereqs
		Assembly.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func
		native_getTime=Assembly.getTime
		Assembly.getTime=self.dummy_getNumber.im_func
		self.obj.step=Assembly(self.workspace, self.vital_parameters)

		expected=self.dummy_getString() + "/contigs." + self.dummy_getString()
		actual=self.obj.getOutputFile()

		Summarize.getStepDir=native_getStepDir
		Summarize.getOutputFileExtension=native_getOutputFileExtension
		Assembly.autoGeneratePrereqs=native_autoGeneratePrereqs
		Assembly.getTime=native_getTime

		self.assertEqual(expected, actual)

	def test_getOutputFile_refineA(self):
		native_getStepDir=Summarize.getStepDir
		Summarize.getStepDir=self.dummy_getString.im_func
		native_getOutputFileExtension=Summarize.getOutputFileExtension
		Summarize.getOutputFileExtension=self.dummy_getString.im_func
		native_autoGeneratePrereqs=Assembly.autoGeneratePrereqs
		Assembly.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func
		native_getTime=Assembly.getTime
		Assembly.getTime=self.dummy_getNumber.im_func
		native_autoGeneratePrereqs_refineA=RefineA.autoGeneratePrereqs
		RefineA.autoGeneratePrereqs=self.dummy_autoGeneratePrereqs.im_func
		self.obj.step=RefineA(self.workspace, self.vital_parameters)

		expected=self.dummy_getString() + "/contigs." + self.dummy_getString()
		actual=self.obj.getOutputFile()

		Summarize.getStepDir=native_getStepDir
		Summarize.getOutputFileExtension=native_getOutputFileExtension
		Assembly.autoGeneratePrereqs=native_autoGeneratePrereqs
		Assembly.getTime=native_getTime
		RefineA.autoGeneratePrereqs=native_autoGeneratePrereqs_refineA

		self.assertEqual(expected, actual)
		
	def test_getOutputFileExtension(self):
		self.assertEqual("list", self.obj.getOutputFileExtension())

	def test_getMem(self):
		Mock.getSmallMemory=self.dummy_getNumber.im_func
		self.workspace.resources=Mock()

		actual=self.obj.getMem()

		del self.workspace.resources
		del Mock.getSmallMemory

		self.assertEqual(self.dummy_getNumber(), actual)

	def test_getTime(self):
		Mock.getSmallTime=self.dummy_getNumber.im_func
		self.workspace.resources=Mock()

		actual=self.obj.getTime()

		del self.workspace.resources
		del Mock.getSmallTime

		self.assertEqual(self.dummy_getNumber(), actual)

	def test_getThread(self):
		self.assertEqual(1, self.obj.getThreads())

class tGenericAssembly(unittest.TestCase):
	workspace=Mock(work_dir="work_dir", input_file="input_file")
	vital_parameters=Mock(fp=1.5, fn=.150, pval=1e-5, min_molecule_len=100, min_molecule_sites=6)
	def dummy_autoGen(self):
		self.autoGenCalled=True
	def test_createAssembly_assembly(self):
		native_autoGen=Assembly.autoGeneratePrereqs
		Assembly.autoGeneratePrereqs=self.dummy_autoGen.im_func
		expected=Assembly(self.workspace, self.vital_parameters)

		actual=GenericAssembly.createAssembly(self.workspace, self.vital_parameters, "assembly")

		Assembly.autoGeneratePrereqs=native_autoGen

		self.assertEqual(expected, actual)

	def test_createAssembly_refineA(self):
		native_autoGen=RefineA.autoGeneratePrereqs
		RefineA.autoGeneratePrereqs=self.dummy_autoGen.im_func
		expected=RefineA(self.workspace, self.vital_parameters)

		actual=GenericAssembly.createAssembly(self.workspace, self.vital_parameters, "refineA")

		RefineA.autoGeneratePrereqs=native_autoGen

		self.assertEqual(expected, actual)

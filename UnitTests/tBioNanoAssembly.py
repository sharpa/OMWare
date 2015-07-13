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
import UnitTests.Helper
from Operations.BioNano.file_bnx import BnxFile
from Operations.BioNano.Assemble.RefineA import RefineA
from Operations.BioNano.Assemble.Assembly import Assembly
from Operations.BioNano.Assemble.Summarize import Summarize
from Operations.BioNano.Assemble.GroupManifest import GroupManifest
from Operations.BioNano.Assemble.Sort import Sort
from Operations.BioNano.Assemble.Split import Split
from Operations.BioNano.Assemble.PairwiseAlignment import PairwiseAlignment
from Operations.BioNano.Assemble.MoleculeStats import MoleculeStats
from Operations.BioNano.Assemble.Input import Input

class tAssembly(unittest.TestCase):
	workspace=UnitTests.Helper.Mock(input_file="input_file", work_dir="work_dir")
	vital_parameters=UnitTests.Helper.Mock(pval="pval", fp="fp", fn="fn", min_molecule_len="minlen", min_molecule_sites="minsites")
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
		self.workspace.binaries={"bng_assembler": "Assembler"}
		native_getStepDir=Assembly.getStepDir
		Assembly.getStepDir=self.dummy_getStepDir.im_func
		native_getMem=Assembly.getMem
		Assembly.getMem=self.dummy_getResources.im_func
		native_getThreads=Assembly.getThreads
		Assembly.getThreads=self.dummy_getResources.im_func
		UnitTests.Helper.Mock.getListFile=self.dummy_getOutputFile.im_func
		UnitTests.Helper.Mock.getOutputFile=self.dummy_getOutputFile.im_func
		self.obj.split=UnitTests.Helper.Mock()
		self.obj.pairwise_alignment=UnitTests.Helper.Mock()
		self.obj.molecule_stats=UnitTests.Helper.Mock()
		
		expected=["cd " + self.workspace.work_dir + "\n" +
			"mkdir " + self.dummy_getStepDir() + "\n" +
			"cd " + self.dummy_getStepDir() + "\n" +
			"pwd\n" +
			"Assembler -if ../output_file -af ../output_file -XmapStatRead ../output_file -usecolor 1 -FP fp -FN fn -sd 0.2 -sf 0.2 -sr 0.03 -res 3.3 -T pval -S 1 -MaxRelCoverage 100 200 30 -BulgeCoverage 20 -MaxCoverage 10 -MinCov 10 -MinAvCov 5 -MinMaps 5 -MinContigLen 0.0 -EndTrim 1 -refine 0 -PVchim 0.001 3 -FastBulge 1000 -FragilePreserve 0 -draftsize 1 -SideBranch 1 -contigs_format 1 -maxthreads -1 -maxmem 1 -minlen minlen -minsites minsites -minSNR 2 -o unrefined -AlignmentFilter 100 2.0 0.5 -force  -SideChain  -stdout  -stderr \n" +
			"result=`tail -n 1 ../" + self.dummy_getStepDir() + "/" + self.obj.output_prefix + ".stdout`\n" +
			"if [[ \"$result\" != \"END of output\" ]]; then exit 1; else touch Complete.status; fi\n"]

		actual=self.obj.writeCode()

		del self.workspace.binaries
		Assembly.getStepDir=native_getStepDir
		Assembly.getMem=native_getMem
		Assembly.getThreads=native_getThreads
		del UnitTests.Helper.Mock.getListFile
		del UnitTests.Helper.Mock.getOutputFile

		self.assertEqual(expected, actual)

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
		Assembly.autoGeneratePrereqs=self.native_autoGeneratePrereqs
		native_getTime_split=Split.getTime
		Split.getTime=self.dummy_getLargeMemory.im_func
		native_getTime_pairwise=PairwiseAlignment.getTime
		PairwiseAlignment.getTime=self.dummy_getLargeMemory.im_func
		self.obj.vital_parameters.blocks=1
		self.vital_parameters.blocks=1

		expected_sort=Sort(self.workspace, copy(self.vital_parameters))
		expected=[Input(self.workspace), expected_sort, expected_sort.getMoleculeStats(), Split(self.workspace, copy(self.vital_parameters)), PairwiseAlignment(self.workspace, copy(self.vital_parameters))]

		self.obj.autoGeneratePrereqs()

		Split.getTime=native_getTime_split
		PairwiseAlignment.getTime=native_getTime_pairwise
		del self.obj.vital_parameters.blocks

		self.assertEqual(expected, [self.obj.inpt, self.obj.sort, self.obj.molecule_stats, self.obj.split, self.obj.pairwise_alignment])

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

class tInput(unittest.TestCase):
	workspace=UnitTests.Helper.Mock(work_dir="work_dir", input_file="input_file")
	def setUp(self):
		self.obj=Input(self.workspace)
	def test_init_default(self):
		expected=[self.workspace, None]
		self.assertEqual(expected, [self.obj.workspace, self.obj.quality])

	def test_hash(self):
		expected=hash((self.workspace.input_file, self.workspace.work_dir, "Input"))
		self.assertEqual(expected, self.obj.__hash__())

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
	def test_getPrereqs(self):
		self.assertEqual([], self.obj.getPrereqs())

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
		self.quality=UnitTests.Helper.Mock(createCalled=True, count=1, quantity=2, labels=3, density=4, average=5)

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
		quality=UnitTests.Helper.Mock(count=1)
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
		quality=UnitTests.Helper.Mock(quantity=1)
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
		quality=UnitTests.Helper.Mock(labels=1)
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
		self.obj.quality=UnitTests.Helper.Mock(labels=2, quantity=1.0)
		expected = 2 / 1.0

		self.assertEqual(expected, self.obj.loadQuality_density())
	def test_loadQuality_density_qualityWithDensity(self):
		self.obj.quality=UnitTests.Helper.Mock(labels=2, quantity=1.0, density=10)
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
		self.obj.quality=UnitTests.Helper.Mock(count=2, quantity=4.0)
		expected = 4.0 / 2

		self.assertEqual(expected, self.obj.loadQuality_averageLength())
	def test_loadQuality_averageLength_qualityWithDensity(self):
		self.obj.quality=UnitTests.Helper.Mock(count=2, quantity=4.0, average=10)
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
		return [ UnitTests.Helper.Mock(length=100.0, num_labels=13),
			UnitTests.Helper.Mock(length=200.0, num_labels=26),
			UnitTests.Helper.Mock(length=300.0, num_labels=39) ]

class tRefineA(unittest.TestCase):
	workspace=UnitTests.Helper.Mock(work_dir="work_dir", input_file="input_file")
	vital_parameters=UnitTests.Helper.Mock(fp="fp", fn="fn", pval="pval", min_molecule_len="minlen", min_molecule_sites="minsites")
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
	def dummy_getPrereqs(self):
		return [UnitTests.Helper.Mock()]
	def dummy_getOutputFile(self):
		return "output_file.ext"
	def test_constructor_default(self):
		expected=UnitTests.Helper.Mock(
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
			output_prefix="refineeA",
			send_output_to_file=True,
			send_errors_to_file=True,
			autoGeneratePrereqsCalled=True)

		self.assertEqual(expected, self.obj)

	def test_writeCode(self):
		self.workspace.binaries={"bng_assembler": "Assembler"}
		native_getStepDir=RefineA.getStepDir
		RefineA.getStepDir=self.dummy_getStepDir.im_func
		native_getThreads=RefineA.getThreads
		RefineA.getThreads=self.dummy_getResources.im_func
		native_getPrereqs=RefineA.getPrereqs
		RefineA.getPrereqs=self.dummy_getPrereqs.im_func
		UnitTests.Helper.Mock.getOutputFile=self.dummy_getOutputFile.im_func
		self.obj.sort=UnitTests.Helper.Mock()
		self.obj.assembly=UnitTests.Helper.Mock()
		self.obj.molecule_stats=UnitTests.Helper.Mock()

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
			"  group_start=`echo $line | awk '{print $2}'`\n" +
			"  group_end=`echo $line | awk '{print $3}'`\n" +
			"    Assembler -i ../output_file.ext -contigs ../output_file.ext $group_start $group_end -maxthreads -1 -T pval -usecolor 1 -extend 1 -refine 2 -MultiMode  -EndTrim 0.99 -LRBias 100.0 -Mprobeval  -deltaX 4 -deltaY 6 -outlier 1e-05 -endoutlier 1e-05 -contigs_format 1 -force  -FP fp -FN fn -sd 0.2 -sf 0.2 -sr 0.03 -res 3.3 -output_prefix refineeA -stdout  -stderr  -XmapStatRead ../output_file.ext\n" +
			"done < ../" + self.dummy_getPrereqs()[0].getOutputFile()]

		actual=self.obj.writeCode()
		
		del self.workspace.binaries
		RefineA.getStepDir=native_getStepDir
		RefineA.getThreads=native_getThreads
		RefineA.getPrereqs=native_getPrereqs
		del UnitTests.Helper.Mock.getOutputFile
		
		self.assertEqual(expected, actual)
	def test_getStepDir(self):
		UnitTests.Helper.Mock.getStepDir=self.dummy_getStepDir.im_func
		self.obj.inpt=UnitTests.Helper.Mock()
		expected="refineA_" + self.dummy_getStepDir() + "_fp" + self.vital_parameters.fp + "_fn" + self.vital_parameters.fn + "_pval" + self.vital_parameters.pval + "_minlen" + self.vital_parameters.min_molecule_len + "_minsites" + self.vital_parameters.min_molecule_sites

		actual=self.obj.getStepDir()

		del self.obj.inpt
		del UnitTests.Helper.Mock.getStepDir

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
		sort=Sort(self.workspace, copy(self.vital_parameters))
		expected=RefineA(self.workspace, copy(self.vital_parameters))
		expected.inpt=Input(self.workspace)
		expected.sort=sort
		expected.molecule_stats=sort.getMoleculeStats()
		expected.split=Split(self.workspace, copy(self.vital_parameters))
		expected.pairwise_alignment=PairwiseAlignment(self.workspace, copy(self.vital_parameters))
		expected.assembly=Assembly(self.workspace, copy(self.vital_parameters))
		expected.autoGeneratePrereqsCalled=True

		self.obj.autoGeneratePrereqs()		

		Split.getTime=native_getTime_split
		PairwiseAlignment.getTime=native_getTime_pairwise
		del self.vital_parameters.blocks

		self.assertEqual(expected, self.obj)
	def test_getPrereqs(self):
		assembly=UnitTests.Helper.Mock()
		self.obj.assembly=assembly
		expected=[GroupManifest(self.workspace, assembly)]

		actual=self.obj.getPrereqs()

		self.assertEqual(expected, actual)
	def test_getMem(self):
		UnitTests.Helper.Mock.getMediumMemory=self.dummy_getResources.im_func
		self.obj.workspace.resources=UnitTests.Helper.Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getMem()

		del UnitTests.Helper.Mock.getMediumMemory
		del self.obj.workspace.resources

		self.assertEqual(expected, actual)
	def test_getTime(self):
		UnitTests.Helper.Mock.getLargeTime=self.dummy_getResources.im_func
		self.obj.workspace.resources=UnitTests.Helper.Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getTime()

		del UnitTests.Helper.Mock.getLargeTime
		del self.obj.workspace.resources

		self.assertEqual(expected, actual)
	def test_getThreads(self):
		UnitTests.Helper.Mock.getMediumThreads=self.dummy_getResources.im_func
		self.obj.workspace.resources=UnitTests.Helper.Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getThreads()

		del UnitTests.Helper.Mock.getMediumThreads
		del self.obj.workspace.resources

		self.assertEqual(expected, actual)

class tGroupManifest(unittest.TestCase):
	workspace=UnitTests.Helper.Mock(work_dir="work_dir", input_file="input_file")
	assembly=UnitTests.Helper.Mock(output_prefix="output_prefix", vital_parameters=UnitTests.Helper.Mock(fp="fp", fn="fn", pval="pval", min_molecule_len="minlen", min_molecule_sites="minsites"))
	def setUp(self):
		self.obj=GroupManifest(self.workspace, self.assembly)
	def dummy_getResources(self):
		return -1
	def dummy_getStepDir(self):
		return "step_dir"

	def test_constructor_default(self):
		expected=UnitTests.Helper.Mock(
			workspace=self.workspace,
			assembly=self.assembly,
			quality=None)

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
		expected+="from Operations.BioNano.Assemble.Assembly import Assembly;"
		expected+="from Operations.BioNano.Assemble.GroupManifest import GroupManifest;"
		expected+="ws=Workspace(\"" + self.workspace.work_dir + "\", \"" + self.workspace.input_file + "\");"
		expected+="vp=VitalParameters(" + self.assembly.vital_parameters.fp + ", " + self.assembly.vital_parameters.fn + ", " + self.assembly.vital_parameters.pval + ", " + self.assembly.vital_parameters.min_molecule_len + ", " + self.assembly.vital_parameters.min_molecule_sites + ");"
		expected+="gm=GroupManifest(ws, Assembly(ws, vp));"
		expected+="gm.makeGroupManifestFile()'"

		actual=self.obj.writeCode()

		GroupManifest.getStepDir=native_getStepDir
		
		self.assertEqual([expected], actual)

	def test_getStepDir(self):
		UnitTests.Helper.Mock.getStepDir=self.dummy_getStepDir.im_func
		expected="manifest_for_" + self.dummy_getStepDir()

		actual=self.obj.getStepDir()

		del UnitTests.Helper.Mock.getStepDir
		self.assertEqual(expected, actual)
	def test_getOutputFile(self):
		native_getStepDir=GroupManifest.getStepDir
		GroupManifest.getStepDir=self.dummy_getStepDir.im_func
		UnitTests.Helper.Mock.getStepDir=self.dummy_getStepDir.im_func
		expected=self.dummy_getStepDir() + self.assembly.output_prefix + ".group_manifest"

		actual=self.obj.getOutputFile()

		GroupManifest.getStepDir=native_getStepDir
		del UnitTests.Helper.Mock.getStepDir
		self.assertEqual(expected, actual)

	def test_getOutputFileExtension(self):
		self.assertEqual("group_manifest", self.obj.getOutputFileExtension())
	def test_autoGeneratePrereqs(self):
		self.obj.autoGeneratePrereqs()
	def test_getPrereqs(self):
		self.assertEqual([self.assembly], self.obj.getPrereqs())

	def test_getMem(self):
		UnitTests.Helper.Mock.getSmallMemory=self.dummy_getResources.im_func
		self.obj.workspace.resources=UnitTests.Helper.Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getMem()

		del self.obj.workspace.resources
		del UnitTests.Helper.Mock.getSmallMemory

		self.assertEqual(expected, actual)
	def test_getTime(self):
		UnitTests.Helper.Mock.getSmallTime=self.dummy_getResources.im_func
		self.obj.workspace.resources=UnitTests.Helper.Mock()
		expected=self.dummy_getResources()

		actual=self.obj.getTime()

		del self.obj.workspace.resources
		del UnitTests.Helper.Mock.getSmallTime

		self.assertEqual(expected, actual)
	def test_getThreads(self):
		self.assertEqual(1, self.obj.getThreads())

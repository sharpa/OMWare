# Module: UnitTests.tOperations
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/26/2015
# 
# The purpose of this module is to provide unit tests for
# classes that are directly in the Operations module (not submodules)
import unittest
import os
import copy
from UnitTests.Helper import Mock
from Operations.Step import Step
from Operations.Step import Quality

class tStep(unittest.TestCase):
	workspace=Mock(input_file="input_file", work_dir="work_dir")
	vital_parameters=Mock(pval=1e-5, fp=1.5, fn=.150, min_molecule_len=100, min_molecule_sites=6)
	native_autoGeneratePrereqs=Step.autoGeneratePrereqs

	def dummy_autoGeneratePrereqs(self):
		self.autoGeneratePrereqsCalled=True
	def dummy_getStepDir(self):
		return "tmp"
	def dummy_isComplete_true(self):
		return True
	def dummy_isComplete_false(self):
		return False
	def dummy_getQualityFileName(self):
		return "Quality.json"
	def dummy_createQualityObject(self):
		self.quality=Quality()
	def dummy_createQualityObject_wSave(self):
		self.quality=Quality(key="value")
		native_getQualityFileName=Step.getQualityFileName
		Step.getQualityFileName=tStep.dummy_getQualityFileName.im_func

		self.saveQualityObjectToFile()

		Step.getQualityFileName=native_getQualityFileName
	def dummy_loadQualityReportItems(self):
		return {"1": 1, "2": 2, "1.0": 1, "4": 4, "3": 3}

	def setUp(self):
		Step.autoGeneratePrereqs=tStep.dummy_autoGeneratePrereqs.im_func
		self.obj=Step(self.workspace, self.vital_parameters)

	def tearDown(self):
		Step.autoGeneratePrereqs=self.native_autoGeneratePrereqs
	
	def test_constructor(self):
		self.assertEqual([self.workspace, self.vital_parameters, None, True], [self.obj.workspace, self.obj.vital_parameters, self.obj.quality, self.obj.autoGeneratePrereqsCalled])

	def test_hash(self):
		class_name="Step"
		expected=hash((self.workspace.input_file, self.workspace.work_dir, self.vital_parameters.pval, self.vital_parameters.fp, self.vital_parameters.fn, self.vital_parameters.min_molecule_len, self.vital_parameters.min_molecule_sites, class_name))

		self.assertEqual(expected, self.obj.__hash__())

	def test_eq(self):
		obj_copy=copy.deepcopy(self.obj)
		before_change=obj_copy==self.obj
		self.obj.dummy_var="dummy"
		after_change_one=obj_copy==self.obj
		obj_copy.dummy_var="dummy"
		after_change_two=obj_copy==self.obj
		
		self.assertEqual([True, False, True], [before_change, after_change_one, after_change_two])

	def test_ne(self):
		obj_copy=copy.deepcopy(self.obj)
		before_change=obj_copy!=self.obj
		self.obj.dummy_var="dummy"
		after_change_one=obj_copy!=self.obj
		obj_copy.dummy_var="dummy"
		after_change_two=obj_copy!=self.obj
		
		self.assertEqual([False, True, False], [before_change, after_change_one, after_change_two])

	def test_str(self):
		expected="{'min_molecule_sites': " + str(self.vital_parameters.min_molecule_sites) + ", 'fp': " + str(self.vital_parameters.fp) + ", 'min_molecule_len': " + str(self.vital_parameters.min_molecule_len) + ", 'fn': " + str(self.vital_parameters.fn) + ", 'pval': " + str(self.vital_parameters.pval) + "}"
		self.assertEqual(expected,str(self.obj))

	def test_write_code(self):
		with self.assertRaises(Exception):
			self.obj.writeCode()

	def test_get_step_dir(self):
		with self.assertRaises(Exception):
			self.obj.getStepDir()

	def test_get_output_file_extension(self):
		with self.assertRaises(Exception):
			self.obj.getOutputFileExtension()

	def test_auto_generate_prereqs(self):
		Step.autoGeneratePrereqs=self.native_autoGeneratePrereqs
		with self.assertRaises(Exception):
			self.obj.autoGeneratePrereqs()

	def test_get_prereq(self):
		with self.assertRaises(Exception):
			self.obj.getPrereq()

	def test_is_complete_while_is(self):
		native_getStepDir=Step.getStepDir
		Step.getStepDir=tStep.dummy_getStepDir.im_func
		actual=-1
		
		os.mkdir("tmp")
		with open("tmp/Complete.status", "w"):
			actual=self.obj.isComplete()

		os.remove("tmp/Complete.status")
		os.rmdir("tmp")
		Step.getStepDir=native_getStepDir

		self.assertEqual(True, actual)

	def test_is_complete_while_is_not(self):
		native_getStepDir=Step.getStepDir
		Step.getStepDir=tStep.dummy_getStepDir.im_func

		actual=self.obj.isComplete()
		
		Step.getStepDir=native_getStepDir

		self.assertEqual(False, actual)


	def test_getQualityFileName(self):
		native_getStepDir=Step.getStepDir
		Step.getStepDir=tStep.dummy_getStepDir.im_func
		expected=self.dummy_getStepDir() + "/Quality.json"

		actual=self.obj.getQualityFileName()

		Step.getStepDir=native_getStepDir

		self.assertEqual(expected, actual)
		
	def dummy_loadQualityObjectFromFile(self):
		self.quality=Mock(dummy=True)

	def test_loadQualityReport_noQuality_cutoff1(self):
		native_loadQualityObjectFromFile=Step.loadQualityObjectFromFile
		Step.loadQualityObjectFromFile=tStep.dummy_loadQualityObjectFromFile.im_func
		native_loadQualityReportItems=Step.loadQualityReportItems
		Step.loadQualityReportItems=tStep.dummy_loadQualityReportItems.im_func
		expecteds=[["1", "1.0"], Mock(dummy=True)]
		actuals=[
			self.obj.loadQualityReport(1),
			self.obj.quality
		]

		Step.loadQualityObjectFromFile=native_loadQualityObjectFromFile
		Step.loadQualityReportItems=native_loadQualityReportItems

		self.assertEqual(expecteds, actuals)
		
	def test_loadQualityReport_quality_cutoff2(self):
		self.obj.quality=Mock(dummy=False)
		native_loadQualityReportItems=Step.loadQualityReportItems
		Step.loadQualityReportItems=tStep.dummy_loadQualityReportItems.im_func
		expecteds=[["1", "2", "1.0"], Mock(dummy=False)]

		actuals=[
			self.obj.loadQualityReport(2),
			self.obj.quality
		]

		Step.loadQualityReportItems=native_loadQualityReportItems

		self.assertEqual(expecteds, actuals)

	def test_loadQualityReport_quality_cutoff1(self):
		self.obj.quality=Mock(dummy=False)
		native_loadQualityReportItems=Step.loadQualityReportItems
		Step.loadQualityReportItems=tStep.dummy_loadQualityReportItems.im_func
		expecteds=[["1", "1.0"], Mock(dummy=False)]

		actuals=[
			self.obj.loadQualityReport(1),
			self.obj.quality
		]

		Step.loadQualityReportItems=native_loadQualityReportItems

		self.assertEqual(expecteds, actuals)

	def test_loadQualityReport_quality_cutoff0(self):
		self.obj.quality=Mock(dummy=False)
		native_loadQualityReportItems=Step.loadQualityReportItems
		Step.loadQualityReportItems=tStep.dummy_loadQualityReportItems.im_func
		expecteds=[[], Mock(dummy=False)]

		actuals=[
			self.obj.loadQualityReport(0),
			self.obj.quality
		]

		Step.loadQualityReportItems=native_loadQualityReportItems

		self.assertEqual(expecteds, actuals)

	def test_create_quality_object(self):
		with self.assertRaises(Exception):
			self.obj.createQualityObject()

	def test_load_quality_report_items(self):
		with self.assertRaises(Exception):
			self.obj.loadQualityReportItems()

	def test_saveQualityObjectToFile_objectDoesNotExist(self):
		native_createQualityObject=Step.createQualityObject
		Step.createQualityObject=tStep.dummy_createQualityObject.im_func
		native_getQualityFileName=Step.getQualityFileName
		Step.getQualityFileName=tStep.dummy_getQualityFileName.im_func

		self.obj.saveQualityObjectToFile()

		Step.createQualityObject=native_createQualityObject
		Step.getQualityFileName=native_getQualityFileName

		expected="{}"
		actual=""
		with open(self.dummy_getQualityFileName()) as qual_file:
			actual=qual_file.read()
		os.remove(self.dummy_getQualityFileName())
		
		self.assertEqual(expected, actual)

	def test_saveQualityObjectToFile_objectDoesExist(self):
		native_getQualityFileName=Step.getQualityFileName
		Step.getQualityFileName=tStep.dummy_getQualityFileName.im_func
		self.obj.quality=Quality(key="value")

		self.obj.saveQualityObjectToFile()

		Step.getQualityFileName=native_getQualityFileName

		expected="{\n \"key\": \"value\"\n}"
		actual=""
		with open(self.dummy_getQualityFileName()) as qual_file:
			actual=qual_file.read()
		os.remove(self.dummy_getQualityFileName())
		
		self.assertEqual(expected, actual)

	def test_loadQualityObjectFromFile_fileDoesExist(self):
		native_getQualityFileName=Step.getQualityFileName
		Step.getQualityFileName=tStep.dummy_getQualityFileName.im_func
		with open(self.dummy_getQualityFileName(), "w") as quality_file:
			quality_file.write("{\n \"key\": \"value\"\n}")

		self.obj.loadQualityObjectFromFile()

		Step.getQualityFileName=native_getQualityFileName
		os.remove(self.dummy_getQualityFileName())

		self.assertEqual(Quality(key="value"), self.obj.quality)

	def test_loadQualityObjectFromFile_fileDoesNotExist(self):
		native_getQualityFileName=Step.getQualityFileName
		Step.getQualityFileName=tStep.dummy_getQualityFileName.im_func
		native_createQualityObject=Step.createQualityObject
		Step.createQualityObject=tStep.dummy_createQualityObject_wSave.im_func

		self.obj.loadQualityObjectFromFile()

		Step.getQualityFileName=native_getQualityFileName
		Step.createQualityObject=native_createQualityObject
		os.remove(self.dummy_getQualityFileName())

		self.assertEqual(Quality(key="value"), self.obj.quality)

	def test_get_mem(self):
		with self.assertRaises(Exception):
			self.obj.getMem()
	def test_get_time(self):
		with self.assertRaises(Exception):
			self.obj.getTime()
	def test_get_threads(self):
		with self.assertRaises(Exception):
			self.obj.getThreads()

	def test_get_error_notification_email(self):
		self.obj.workspace.errorNotificationEmail=None
		actual1=self.obj.getErrorNotificationEmail()
		email="address@domain.com"
		self.obj.workspace.errorNotificationEmail=email
		actual2=self.obj.getErrorNotificationEmail()
		
		self.assertEqual([None, email], [actual1, actual2])

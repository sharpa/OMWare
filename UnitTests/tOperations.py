# Module: UnitTests.tOperations
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/26/2015
# 
# The purpose of this module is to provide unit tests for
# classes that are directly in the Operations module (not submodules)
import unittest
import UnitTests.Helper
import os
import copy
import Operations.Step

class tStep(unittest.TestCase):
	workspace=UnitTests.Helper.Mock(input_file="input_file", work_dir="work_dir")
	vital_parameters=UnitTests.Helper.Mock(pval="pval", fp="fp", fn="fn", min_molecule_len="minlen", min_molecule_sites="minsites")
	native_autoGeneratePrereqs=Operations.Step.Step.autoGeneratePrereqs

	def dummy_autoGeneratePrereqs(self):
		self.autoGeneratePrereqsCalled=True
	def dummy_getStepDir(self):
		return "tmp"

	def setUp(self):
		Operations.Step.Step.autoGeneratePrereqs=tStep.dummy_autoGeneratePrereqs.im_func
		self.obj=Operations.Step.Step(self.workspace, self.vital_parameters)

	def tearDown(self):
		Operations.Step.Step.autoGeneratePrereqs=self.native_autoGeneratePrereqs
	
	def test_constructor(self):
		self.assertEqual([self.workspace, self.vital_parameters, True], [self.obj.workspace, self.obj.vital_parameters, self.obj.autoGeneratePrereqsCalled])

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
		expected="{'min_molecule_sites': 'minsites', 'fp': 'fp', 'min_molecule_len': 'minlen', 'fn': 'fn', 'pval': 'pval'}"
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
		Operations.Step.Step.autoGeneratePrereqs=self.native_autoGeneratePrereqs
		with self.assertRaises(Exception):
			self.obj.autoGeneratePrereqs()

	def test_get_prereqs(self):
		with self.assertRaises(Exception):
			self.obj.getPrereqs()

	def test_is_complete_while_is(self):
		native_getStepDir=Operations.Step.Step.getStepDir
		Operations.Step.Step.getStepDir=tStep.dummy_getStepDir.im_func
		
		os.mkdir("tmp")
		with open("tmp/Complete.status", "w"):
			self.assertEqual(True, self.obj.isComplete())

		os.remove("tmp/Complete.status")
		os.rmdir("tmp")

	def test_is_complete_while_is_not(self):
		native_getStepDir=Operations.Step.Step.getStepDir
		Operations.Step.Step.getStepDir=tStep.dummy_getStepDir.im_func
		
		self.assertEqual(False, self.obj.isComplete())

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

# Module: UnitTests.tUtils.py
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/25/2015
# 
# The purpose of this module is to provide unit tests for Utils
import unittest
from UnitTests.Helper import Mock
import os
from copy import copy
import Utils.CD
import Utils.Resources
import Utils.MacbookProResources
import Utils.FultonResources
import Utils.FultonResourcesLight
import Utils.Workspace

class tCD(unittest.TestCase):
	def setUp(self):
		os.makedirs("tmp")
	def tearDown(self):
		os.rmdir("tmp")
	def test_directory_exists(self):
		base=os.getcwd()
		with Utils.CD.CD("tmp"):
			self.assertEqual(base+"/tmp", os.getcwd())
		self.assertNotEqual(base+"/tmp", os.getcwd())
	def test_directory_does_not_exist(self):
		with self.assertRaises(OSError):
			with Utils.CD.CD("tmp_1"):
				pass

class tResources(unittest.TestCase):
	def setUp(self):
		self.obj=Utils.Resources.Resources()

	def test_get_small_memory(self):
		with self.assertRaises(Exception):
			self.obj.getSmallMemory()
	def test_get_medium_memory(self):
		with self.assertRaises(Exception):
			self.obj.getMediumMemory()
	def test_get_large_memory(self):
		with self.assertRaises(Exception):
			self.obj.getLargeMemory()

	def test_get_small_time(self):
		with self.assertRaises(Exception):
			self.obj.getSmallTime()
	def test_get_medium_time(self):
		with self.assertRaises(Exception):
			self.obj.getMediumTime()
	def test_get_large_time(self):
		with self.assertRaises(Exception):
			self.obj.getLargeTime()

	def test_get_small_threads(self):
		with self.assertRaises(Exception):
			self.obj.getSmallThreads()
	def test_get_medium_threads(self):
		with self.assertRaises(Exception):
			self.obj.getMediumThreads()
	def test_get_large_threads(self):
		with self.assertRaises(Exception):
			self.obj.getLargeThreads()

class tMacbookProResources(unittest.TestCase):
	def setUp(self):
		self.obj=Utils.MacbookProResources.Resources()

	def test_get_small_memory(self):
		self.assertEqual(1, self.obj.getSmallMemory())
	def test_get_medium_memory(self):
		self.assertEqual(3, self.obj.getMediumMemory())
	def test_get_large_memory(self):
		self.assertEqual(7, self.obj.getLargeMemory())

	def test_get_small_time(self):
		self.assertEqual(24, self.obj.getSmallTime())
	def test_get_medium_time(self):
		self.assertEqual(4392, self.obj.getMediumTime())
	def test_get_large_time(self):
		self.assertEqual(8760, self.obj.getLargeTime())

	def test_get_small_threads(self):
		self.assertEqual(1, self.obj.getSmallThreads())
	def test_get_medium_threads(self):
		self.assertEqual(1, self.obj.getMediumThreads())
	def test_get_large_threads(self):
		self.assertEqual(2, self.obj.getLargeThreads())

class tFultonResources(unittest.TestCase):
	def setUp(self):
		self.obj=Utils.FultonResources.Resources()

	def test_eq_None(self):
		other=None
		expected=[False, True]

		actual=[
			self.obj==other,
			self.obj!=other
		]

		self.assertEqual(expected, actual)

	def test_eq_diffClass(self):
		other=Mock()
		expected=[False, True]

		actual=[
			self.obj==other,
			self.obj!=other
		]

		self.assertEqual(expected, actual)

	def test_eq_sameClass(self):
		other=Utils.FultonResources.Resources()
		expected=[True, False]

		actual=[
			self.obj==other,
			self.obj!=other
		]

		self.assertEqual(expected, actual)

	def test_get_small_memory(self):
		self.assertEqual(1, self.obj.getSmallMemory())
	def test_get_medium_memory(self):
		self.assertEqual(8, self.obj.getMediumMemory())
	def test_get_large_memory(self):
		self.assertEqual(24, self.obj.getLargeMemory())

	def test_get_small_time(self):
		self.assertEqual(1, self.obj.getSmallTime())
	def test_get_medium_time(self):
		self.assertEqual(12, self.obj.getMediumTime())
	def test_get_large_time(self):
		self.assertEqual(24, self.obj.getLargeTime())

	def test_get_small_threads(self):
		self.assertEqual(2, self.obj.getSmallThreads())
	def test_get_medium_threads(self):
		self.assertEqual(6, self.obj.getMediumThreads())
	def test_get_large_threads(self):
		self.assertEqual(12, self.obj.getLargeThreads())

class tFultonResourcesLight(unittest.TestCase):
	def setUp(self):
		self.obj=Utils.FultonResourcesLight.Resources()

	def test_get_small_memory(self):
		self.assertEqual(1, self.obj.getSmallMemory())
	def test_get_medium_memory(self):
		self.assertEqual(1, self.obj.getMediumMemory())
	def test_get_large_memory(self):
		self.assertEqual(1, self.obj.getLargeMemory())

	def test_get_small_time(self):
		self.assertEqual(1, self.obj.getSmallTime())
	def test_get_medium_time(self):
		self.assertEqual(1, self.obj.getMediumTime())
	def test_get_large_time(self):
		self.assertEqual(1, self.obj.getLargeTime())

	def test_get_small_threads(self):
		self.assertEqual(2, self.obj.getSmallThreads())
	def test_get_medium_threads(self):
		self.assertEqual(2, self.obj.getMediumThreads())
	def test_get_large_threads(self):
		self.assertEqual(2, self.obj.getLargeThreads())

class tWorkspace(unittest.TestCase):
	def test_constructor(self):
		work_dir="work_dir"
		input_file="input_file"
		obj=Utils.Workspace.Workspace(work_dir, input_file)
		self.assertEqual([work_dir, input_file, {}, Utils.FultonResources.Resources().__class__, None], [obj.work_dir, obj.input_file, obj.binaries, obj.resources.__class__, obj.errorNotificationEmail])

	def test_eq_None(self):
		other=None
		obj=Utils.Workspace.Workspace("work_dir", "input_file")
		expected=[False, True]

		actual=[
			obj==other,
			obj!=other
		]

		self.assertEqual(expected, actual)

	def test_eq_notEq(self):
		obj=Utils.Workspace.Workspace("work_dir", "input_file")
		other=Utils.Workspace.Workspace("diff_dir", "diff_file")
		expected=[False, True]

		actual=[
			obj==other,
			obj!=other
		]

		self.assertEqual(expected, actual)

	def test_eq_eq(self):
		obj=Utils.Workspace.Workspace("work_dir", "input_file")
		other=Utils.Workspace.Workspace("work_dir", "input_file")
		expected=[True, False]

		actual=[
			obj==other,
			obj!=other
		]

		self.assertEqual(expected, actual)
		

	def test_error_notification_email(self):
		test_email="address@domain.com"
		obj=Utils.Workspace.Workspace("work_dir", "input_file")
		before_change=obj.errorNotificationEmail
		obj.errorNotificationEmail=test_email
		after_change=obj.errorNotificationEmail
		self.assertEqual([None, test_email], [before_change, after_change])

	def test_add_binary(self):
		obj=Utils.Workspace.Workspace("work_dir", "input_file")
		before_change=copy(obj.binaries)
		obj.addBinary("name1", "path1")
		with_one=copy(obj.binaries)
		obj.addBinary("name2", "path2")
		with_two=copy(obj.binaries)
		obj.addBinary("name1", "path2")
		after_overwrite=copy(obj.binaries)

		self.assertEqual([{}, {"name1": "path1"}, {"name1": "path1", "name2": "path2"}, {"name1": "path2", "name2": "path2"}], [before_change, with_one, with_two, after_overwrite])

# Module: UnitTests.TestAll.py
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/25/2015
# 
# The purpose of this module is to provie unit tests for Utils
import unittest
import os
import Utils.CD

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

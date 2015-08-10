# Module: UnitTests.tFiles
# Version: 0.1
# Author: Aaron Sharp
# Date: 08/10/2015
# 
# The purpose of this module is to provide unit tests for 
# all BioNano file objects

import unittest
import os
from UnitTests.Helper import Mock
from Operations.BioNano.files import File
from Operations.BioNano.files import CmapFile

class tFile_base(unittest.TestCase):
	input_file="file.cmap"
	def setUp(self):
		with open(self.input_file, "w"):
			self.obj=File(self.input_file)

	def tearDown(self):
		os.remove(self.input_file)

class tFile(tFile_base):
	def test_init_fileDoesNotExist(self):
		with self.assertRaises(Exception):
			File("bad_filename")
	def test_init_fileDoesExist(self):
		self.assertEqual(self.input_file, self.obj.input_file)
	def test_equal_otherIsNone(self):
		other=None
		self.assertFalse(self.obj==other)
	def test_equal_otherHasDiffFile(self):
		other_file="other_file.ext"
		with open(other_file, "w"):
			other=File(other_file)
		os.remove(other_file)
		self.assertFalse(self.obj==other)
	def test_equal_sameFile(self):
		other=Mock(input_file=self.input_file)
		self.assertTrue(self.obj==other)

	def test_getExtension(self):
		with self.assertRaises(Exception):
			File.getExtension()

	def test_getHeaders(self):
		expected=["#Header1\n",
			"#Header2\n",
			"#Header3\n",
			"#Header4\n"]
		with open(self.input_file, "w") as i_file:
			i_file.write("".join(expected))
			i_file.write("\n".join(["Non-header1", "#Comment but not header1"]) + "\n")

		actual=self.obj.getHeaders()

		self.assertEqual(expected, actual)

	def test_parse(self):
		with self.assertRaises(Exception):
			self.obj.parse()
	def test_write(self):
		with self.assertRaises(Exception):
			self.obj.write(None, None)

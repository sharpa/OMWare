# Module: UnitTests.TestAll.py
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/25/2015
# 
# The purpose of this module is to provie unit tests for Utils
import unittest

class CD(unittest.TestCase):
	def test_framework(self):
		self.assertEqual(1, 1)
	def test_success(self):
		self.assertNotEqual(1,2)
	def test_fail(self):
		self.assertEqual(1,2)

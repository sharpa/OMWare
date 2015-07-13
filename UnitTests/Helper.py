# Module: UnitTests.Helper.py
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/29/2015
# 
# The purpose of this module is to provide helpful
# odds and ends that multiple test cases will use

class Mock(object):
	def __init__(self, **kwards):
		self.__dict__.update(kwards)
	def __eq__(self, other):
		if other is None:
			return False
		return self.__dict__ == other.__dict__
	def __ne__(self, other):
		return not self == other
	def __str__(self):
		return str(self.__dict__)
	def __repr__(self):
		return str(self)

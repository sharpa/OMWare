# Module: Utils.Resources
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# The purpose of this module is to encapsulate the available
# hardware resources

class Resources():
	def __init__(self):
		pass
	def getMaxThreads(self):
		raise Exception("Abstract method called")
	def getMaxMem(self):
		raise Exception("Abstract method called")

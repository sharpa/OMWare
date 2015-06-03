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

	def getSmallMemory(self):
		raise Exception("Abstract method called")
	def getMediumMemory(self):
		raise Exception("Abstract method called")
	def getLargeMemory(self):
		raise Exception("Abstract method called")

	def getSmallTime(self):
		raise Exception("Abstract method called")
	def getMediumTime(self):
		raise Exception("Abstract method called")
	def getLargeTime(self):
		raise Exception("Abstract method called")

	def getSmallThreads(self):
		raise Exception("Abstract method called")
	def getMediumThreads(self):
		raise Exception("Abstract method called")
	def getLargeThreads(self):
		raise Exception("Abstract method called")

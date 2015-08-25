# Module: Utils.FultonResources
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/03/2015
# 
# The purpose of this module is to encapsulate the available
# hardware resources of the Fulton Supercomputing Lab
import Utils.Resources

class Resources(Utils.Resources.Resources):
	def __init__(self):
		pass
	def __eq__(self,other):
		if other is None:
			return False
		return self.__class__==other.__class__
	def __ne__(self, other):
		return not self==other

	def getSmallMemory(self):
		return 1
	def getMediumMemory(self):
		return 8
	def getLargeMemory(self):
		return 24

	def getSmallTime(self):
		return 1
	def getMediumTime(self):
		return 12
	def getLargeTime(self):
		return 24

	def getSmallThreads(self):
		return 2
	def getMediumThreads(self):
		return 6
	def getLargeThreads(self):
		return 12

# Module: Utils.FultonResourcesLight
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/09/2015
# 
# The purpose of this module is to encapsulate the available
# hardware resources of the Fulton Supercomputing Lab
import Utils.Resources

class Resources(Utils.Resources.Resources):
	def __init__(self):
		pass

	def getSmallMemory(self):
		return 1
	def getMediumMemory(self):
		return 1
	def getLargeMemory(self):
		return 1

	def getSmallTime(self):
		return 1
	def getMediumTime(self):
		return 1
	def getLargeTime(self):
		return 1

	def getSmallThreads(self):
		return 2
	def getMediumThreads(self):
		return 2
	def getLargeThreads(self):
		return 2

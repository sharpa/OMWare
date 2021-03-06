# Module: Utils.MacbookProResources
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# Despite the poor name, this actually only refers to my
# own laptop, on which I am programming this module... Sorry...
import Utils.Resources

class Resources(Utils.Resources.Resources):
	def getSmallMemory(self):
		return 1
	def getMediumMemory(self):
		return 3
	def getLargeMemory(self):
		return 7

	def getSmallTime(self):
		return 24
	def getMediumTime(self):
		return 183*24
	def getLargeTime(self):
		return 365*24

	def getSmallThreads(self):
		return 1
	def getMediumThreads(self):
		return 1
	def getLargeThreads(self):
		return 2


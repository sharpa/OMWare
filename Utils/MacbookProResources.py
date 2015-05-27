# Module: Utils.MacbookProResources
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/27/2015
# 
# Despite the poor name, this actually only refers to my
# own laptop, on which I am programming this module... Sorry...
from Utils.Resources import Resources

class MacbookProResources(Resources):
	def getMaxThreads(self):
		return 2
	def getMaxMem(self):
		return 7

# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/01/2015
# 
# The purpose of this module is encapsulate and provide services for a Workspace
from Utils.FultonResources import Resources

class Workspace:
	def __init__(self, work_dir=None, input_file=None):
		self.work_dir=work_dir
		self.input_file=input_file
		self.binaries={}

		self.resources=Resources()

		self.errorNotificationEmail=None
		
	def addBinary(self, name, path):
		self.binaries[name]=path

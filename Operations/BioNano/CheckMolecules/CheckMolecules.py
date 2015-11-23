# Module: Operations.BioNano.MoleculeChecker.CheckMolecules
# Version: 0.1
# Author: Aaron Sharp
# Date: 11/12/2015
#
# The purpose of this module is to parse alignment data in order to check the quality of the molecules involved

from Operations.Step import Step
class CheckMolecules (Step):
	def __str__(self):
		return str("Check molecules in: " + str(self.workspace) + str(self.vital_parameters.__dict__))

	def writeCode(self):
		code=[]
		code.append("Parse file line")
		code.append("Parse file")
		code.append("Create matrix")
		code.append("For each \"row\", calculate a distribution")
		code.append("Display that ditribution")

		return code

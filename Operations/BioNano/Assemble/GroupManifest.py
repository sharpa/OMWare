# Module: Operations.BioNano.Assemble.GroupManifest
# Version: 0.1
# Author: Aaron Sharp
# Date: 07/08/2015
# 
# The purpose of this module is to WRITE CODE (bash) that will
# run the BNG RefAligner and Assembler software to create an optical map de novo assembly
from Operations.Step import Step

class GroupManifest(Step):
	def __init__(self, workspace, assembly):
		self.workspace=workspace
		self.assembly=assembly
		self.quality=None

	def writeCode(self):
		code="cd " + self.workspace.work_dir + "\n"
		code+="mkdir " + self.getStepDir() + "\n"
		code+="cd " + self.getStepDir() + "\n"
		code+="pwd\n"
		code+="python -c 'from Utils.Workspace import Workspace;"
		code+="from Operations.BioNano.Assemble.VitalParameters import VitalParameters;"
		code+="from Operations.BioNano.Assemble.Assembly import Assembly;"
		code+="from Operations.BioNano.Assemble.GroupManifest import GroupManifest;"
		code+="ws=Workspace(\"" + self.workspace.work_dir + "\", \"" + self.workspace.input_file + "\");"
		code+="vp=VitalParameters(" + str(self.assembly.vital_parameters.fp) + ", " + str(self.assembly.vital_parameters.fn) + ", " + str(self.assembly.vital_parameters.pval) + ", " + str(self.assembly.vital_parameters.min_molecule_len) + ", " + str(self.assembly.vital_parameters.min_molecule_sites) + ");"
		code+="gm=GroupManifest(ws, Assembly(ws, vp));"
		code+="gm.makeGroupManifestFile()'"
		return [code]
		
	def makeGroupManifestFile(self):
		print("I should be making a manifest file right now, but I'm not!")
		
	def getStepDir(self):
		return "manifest_for_" + self.assembly.getStepDir()
	def getOutputFile(self):
		return self.getStepDir() + self.assembly.output_prefix+".group_manifest"
	def getOutputFileExtension(self):
		return "group_manifest"
	def autoGeneratePrereqs(self):
		pass
	def getPrereqs(self):
		return [self.assembly]

	def getMem(self):
		return self.workspace.resources.getSmallMemory()
	def getTime(self):
		return self.workspace.resources.getSmallTime()
	def getThreads(self):
		return 1

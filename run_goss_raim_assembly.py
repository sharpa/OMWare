#!/usr/bin/python

# The purpose of this script is to run a whole assembly
#	with automatic prereg generation

from Assemble.BioNano.BNGAssembly import Assembly
from Assemble.BioNano.BNGVitalParameters import VitalParameters
from Utils.Workspace import Workspace
from Utils.CD import CD
from Assemble.SBATCHCodeFormatter import CodeFormatter

work_dir="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir"
input_file="all.bnx"
workspace=Workspace(work_dir, input_file)
workspace.addBinary("bng_assembler", "/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/Assembler")
workspace.addBinary("bng_ref_aligner", "/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/RefAligner")


vital_parameters=VitalParameters(1.5, .386, 1.11e-6, 100, 10)

assembly=Assembly(workspace, vital_parameters)

with CD(work_dir):
	formatter=CodeFormatter()
	formatter.formatCode(assembly)

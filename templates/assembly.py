#!/usr/bin/python

# The purpose of this script is to run a whole assembly
#	with automatic prereq generation

from Operations.Assemble.BioNano.BNGAssembly import Assembly
from Operations.Assemble.BioNano.BNGVitalParameters import VitalParameters
from Utils.Workspace import Workspace
from Utils.CD import CD
from Operations.SBATCHCodeFormatter import CodeFormatter

work_dir="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir" ### SET ME
input_file="all.bnx" ### SET ME
workspace=Workspace(work_dir, input_file)
workspace.errorNotificationEmail='sharp.aaron.r@gmail.com' ### SET ME
workspace.addBinary("bng_assembler", "/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/Assembler") ### SET ME
workspace.addBinary("bng_ref_aligner", "/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/RefAligner") ### SET ME

false_positives=1.5 ### SET ME
false_negatives=.386 ### SET ME
p_val_cutoff=1.11e-6 ### SET ME
min_molecule_len=100 ### SET ME
min_molecule_sites=10 ### SET ME

vital_parameters=VitalParameters(false_positives, false_negatives, p_val_cutoff, min_molecule_len, min_molecule_sites)

assembly=Assembly(workspace, vital_parameters)

with CD(work_dir):
	formatter=CodeFormatter()
	formatter.serializeCode(assembly)

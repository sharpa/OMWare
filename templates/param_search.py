#!/usr/bin/python

# The purpose of this script is to run an automated param search
from Operations.Parameterize.BNGParameterSearch import ParameterSearch
from Utils.Workspace import Workspace
from Utils.CD import CD
from Operations.SBATCHCodeFormatter import CodeFormatter

work_dir="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir" ### SET ME
input_file="all_very_abridged.bnx" ### SET ME
workspace=Workspace(work_dir, input_file)
workspace.errorNotificationEmail='sharp.aaron.r@gmail.com' ### SET ME
workspace.addBinary("bng_assembler", "/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/Assembler") ### SET ME
workspace.addBinary("bng_ref_aligner", "/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/RefAligner") ### SET ME

genome_size_mb=900 ### SET ME
parameter_search=ParameterSearch(workspace, genome_size_mb)

with CD(work_dir):
	formatter=CodeFormatter()
	formatter.runSeveralSteps(parameter_search.writeCode())
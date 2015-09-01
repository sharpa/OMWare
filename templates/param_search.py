#!/usr/bin/python

# The purpose of this script is to run an automated param search
from Operations.BioNano.Parameterize.ParameterSearch import ParameterSearch
from Utils.Workspace import Workspace
from Utils.CD import CD
from Operations.SBATCHCodeFormatter import CodeFormatter

work_dir="/path/to/work/dir/" ### SET ME
input_file="input_file.bnx" ### SET ME
workspace=Workspace(work_dir, input_file)
workspace.errorNotificationEmail='address@domain.com' ### SET ME
workspace.addBinary("bng_assembler", "/path/to/Assembler") ### SET ME
workspace.addBinary("bng_ref_aligner", "/path/to/RefAligner") ### SET ME

genome_size_mb=900 ### SET ME
parameter_search=ParameterSearch(workspace, genome_size_mb)

#average_label_density=7.0 ### SET ME MAYBE
#expected_label_density=13.5 ### SET ME MAYBE
#parameter_search.optimizeFalsehoods(average_label_density, expected_label_density) ### UNCOMMENT ME MAYBE
#parameter_search.autoGeneratePrereqs() ### UNCOMMENT ME MAYBE

with CD(work_dir):
	formatter=CodeFormatter()
	formatter.runSeveralSteps(parameter_search.writeCode())

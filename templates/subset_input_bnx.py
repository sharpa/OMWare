#!/usr/bin/python

# The purpose of this script is to create subset BNX files

from Operations.Subset.Subsetter import Subsetter
from Utils.Workspace import Workspace
from Utils.CD import CD
from POMMIO import POMMIO

work_dir="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir" ### SET ME
input_file="all_reduced_to_150.bnx" ### SET ME
workspace=Workspace(work_dir, input_file)
workspace.errorNotificationEmail='sharp.aaron.r@gmail.com' ### SET ME
workspace.addBinary("bng_assembler", "/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/Assembler") ### SET ME
workspace.addBinary("bng_ref_aligner", "/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/RefAligner") ### SET ME

with CD(work_dir):
	output_file_name="all_no_runs_1_or_2.bnx" ### SET ME
	subsetter=Subsetter(input_file, output_file_name)

	attribute_to_filter="run_id" ### SET ME
	values_to_remove=["1", "2"] ### SET ME
	subsetter.remove_equals(attribute_to_filter, values_to_remove)

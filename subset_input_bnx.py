#!/usr/bin/python

# The purpose of this script is to create subset BNX files

from Operations.Subset.Subsetter import Subsetter
from Utils.Workspace import Workspace
from Utils.CD import CD
from POMMIO import POMMIO

work_dir="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir"
input_file="all_reduced_to_150.bnx"
workspace=Workspace(work_dir, input_file)
workspace.errorNotificationEmail='sharp.aaron.r@gmail.com'
workspace.addBinary("bng_assembler", "/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/Assembler")
workspace.addBinary("bng_ref_aligner", "/Users/sharpa/Dropbox/Stars/GossRaim_BNG/code/POMM_scratch_input/RefAligner")

with CD(work_dir):
	subsetter=Subsetter(input_file, "all_no_runs_1_or_2.bnx")
	subsetter.remove_equals("run_id", ["1","2"])

#!/usr/bin/python

# The purpose of this script is to characterize a BNG file

from Operations.BioNano.Subset.Subsetter import RunCharacterizer
from Utils.Workspace import Workspace
from Utils.CD import CD
from Operations.BioNano.POMMIO import POMMIO

work_dir="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir" ### SET ME
input_file="all_reduced_to_150.bnx" ### SET ME
workspace=Workspace(work_dir, input_file)

with CD(work_dir):
	characterizer=RunCharacterizer(input_file)
	characterizer.characterize()
	print(characterizer)


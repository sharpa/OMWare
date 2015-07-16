#!/usr/bin/python

# The purpose of this script is to characterize a BNG file

from Operations.BioNano.Subset.Subsetter import RunCharacterizer
from Utils.Workspace import Workspace
from Utils.CD import CD

work_dir="/path/to/work/dir/" ### SET ME
input_file="input_file.bnx" ### SET ME
workspace=Workspace(work_dir, input_file)

with CD(work_dir):
	characterizer=RunCharacterizer(input_file)
	characterizer.characterize()
	print(characterizer)


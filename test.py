#!/usr/bin/python

# The purpose of this test is to run several assemblies
#	to assess the effect of different coverage level
#	by randomly removing molecules


work_dir="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir"
input_file="all_abridged.bnx"

from Utils.Rarefactor import Rarefactor
from Utils.CD import CD
with CD(work_dir):
	obj=Rarefactor(input_file)
	for cutoff in xrange(9, 0, -1):
		obj.generateReducedDataset(float(cutoff)/10)

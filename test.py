#!/usr/bin/python

# The purpose of this test is to run several assemblies
#3	to assess the effect of different coverage level
#	by randomly removing molecules


work_dir="/Users/aaron/Dropbox/Stars/General_BNG/code/POMM_data_dir"
input_file="all_abridged.bnx"

#from Utils.Rarefactor import Rarefactor
from Utils.CD import CD
#with CD(work_dir):
#	obj=Rarefactor(input_file)
#	for cutoff in xrange(9, 0, -1):
#		obj.generateReducedDataset(float(cutoff)/10)

from POMMIO import POMMIO
with CD(work_dir):
	o_file=open("all_abridged.bnx_shrunk", "w")
	pommio=POMMIO(input_file)
	for molecule in pommio.parse("bnx"):
		molecule.shrink(7970.0)
		pommio.write(molecule, o_file, "bnx")

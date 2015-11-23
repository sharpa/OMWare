#!/fslhome/jtpage/bin/python

from sys import argv
if len(argv) < 2:
	print("USAGE: python minimize_alignment.py <list_of_alignments_file> [<significance_filter_(pval_log10)>]")
	exit(1)

sig_filter=0
if len(argv) > 2:
	sig_filter=float(argv[2])

with open(argv[1]) as list_file:
	for file in list_file:
		file=file.strip()
		with open(file) as align_file:
			for line in align_file:
				if line[0]!=">":
					continue

				data=line.split("\t")
				mol1=(data[2])
				mol2=(data[3])
				pval_log10=(data[8])

				if pval_log10 < sig_filter:
					print("\t".join([mol1,mol2,pval_log10]))

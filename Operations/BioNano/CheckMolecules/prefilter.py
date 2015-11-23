#!/fslhome/jtpage/bin/python

from sys import argv

if len(argv) < 4:
	print("USAGE: python prefilter.py <min_len> <min_labels> <mol_stats_file>")
	exit(1)

minlen=float(argv[1])
minsites=float(argv[2])

with open(argv[3]) as stats_file:
	first_line=True
	for line in stats_file:
		if first_line:
			first_line=False
			continue
		data=line.split("\t")
		mol_id=data[0]
		length=float(data[1])
		sites=float(data[2])

		if length>=minlen and sites >= minsites:
			print(mol_id)

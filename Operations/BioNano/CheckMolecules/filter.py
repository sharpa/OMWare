#!/fslhome/jtpage/bin/python

from sys import argv
if len(argv) < 5:
	print("USAGE python filter.py <mol_align_stats_file> <error_around_line_50_default> <line_slope> <line_intercept>")
	exit(1)

with open(argv[1]) as stat_file:
	width=int(argv[2])
	slope=float(argv[3])
	intercept=float(argv[4])

	first_line=True
	for line in stat_file:
		if first_line:
			first_line=False
			continue
		data=line.split("\t")
		mol_id=data[0]
		length=float(data[1])
		count=int(data[2])

		if (count >= (slope*length+intercept)-width) and (count <= (slope*length+intercept)+width):
			print(mol_id)

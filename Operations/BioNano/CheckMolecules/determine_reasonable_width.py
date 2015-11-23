#!/fslhome/jtpage/bin/python

from sys import argv
if len(argv) < 4:
	print("USAGE python determine_reasonable_width.py <mol_align_stats_file> <line_slope> <line_intercept>")
	exit(1)

possible_widths=range(50,1000,10)
results={}
for width in possible_widths:
	results[width]=0.0
with open(argv[1]) as stat_file:
	slope=float(argv[2])
	intercept=float(argv[3])

	first_line=True
	for line in stat_file:
		if first_line:
			first_line=False
			continue
		
		data=line.split("\t")
		mol_id=data[0]
		length=float(data[1])
		count=int(data[2])

		for width in possible_widths:
			if (count >= (slope*length+intercept)-width) and (count <= (slope*length+intercept)+width):
				results[width]+=length
#				results[width]+=1
for width in sorted(results.keys()):
	print(str(width)+"\t"+str(results[width]))

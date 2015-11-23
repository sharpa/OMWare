#!/fslhome/jtpage/bin/python
from sys import argv

if len(argv) < 2:
	print("USAGE: python get_mol_stats.py <bnx_file>")
	exit(1)
with open(argv[1]) as bnx_file:
	print("mol_id	length	labels")
	for line in bnx_file:
		if line[0] != "0":
			continue
		data=line.split("\t")
		mol_id=data[1]
		length=data[2]
		labels=data[5]
		print("\t".join([mol_id,length,labels]))

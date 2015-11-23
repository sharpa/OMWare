#!/fslhome/jtpage/bin/python
from sys import argv

if len(argv) < 3:
	print("USAGE: python get_mol_site_stats.py <minimized_align_file> <mol_stats_file> [<prefiltered_ids>]")
	exit(1)

filter=False
ids=set()
if len(argv) > 3:
	filter=True
	with open(argv[3]) as id_file:
		for line in id_file:
			line=line.strip()
			ids.add(int(line))

site_stats={}
with open(argv[2]) as site_file:
	first_line=True
	for line in site_file:
		if first_line:
			first_line=False
			continue
		data=line.split("\t")
		mol_id=int(data[0])
		sites=int(data[2])
		if filter:
			if mol_id in ids:
				site_stats[mol_id]=sites
		else:
			ids.add(mol_id)
			site_stats[mol_id] = sites

counts={}
with open(argv[1]) as hit_file:
	for line in hit_file:
		data=line.split("\t")
		mol_1=int(data[0])
		mol_2=int(data[1])

		if (mol_1 not in ids) or (mol_2 not in ids):
			continue

		if not mol_1 in counts:
			counts[mol_1]=1
		else:
			counts[mol_1]+=1
		if not mol_2 in counts:
			counts[mol_2]=1
		else:
			counts[mol_2]+=1

print("mol_id\tsites\tcounts")
for key in counts:
	if not key in site_stats:
		print("sites not found: " + str(key))
		continue
	print(str(key)+"\t"+str(site_stats[key])+"\t"+str(counts[key]))

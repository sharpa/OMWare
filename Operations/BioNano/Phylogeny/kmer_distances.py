from sys import argv
if len(argv) < 3:
	print("USAGE: python KmerDistances.py <taxa_cmap_list.txt> <bin_width>")
	exit(1)

from Operations.BioNano.files import CmapFile
from collections import OrderedDict
import re
def calculate_kmer_distribution(taxa, bin_width):
	lengths_file=re.sub('.cmap', '.'+str(bin_width)+'.lengths', taxa)
	try:
		with open(lengths_file) as i_file:
			lengths={}
			for line in i_file:
				line_data=line.split("\t")
				lengths[float(line_data[0])]=int(line_data[1])
			return lengths
	except:
		pass
			
	raw_lengths_file=re.sub('.cmap', '.raw_lengths', taxa)
	raw_lengths=[]
	max_length=-1
	try:
		with open(raw_lengths_file) as i_file:
			for line in i_file:
				raw_lengths=[float(x) for x in line.strip().split("\t")]
			max_length=max(raw_lengths)
	except:
		cmap=CmapFile(taxa)
		current_contig_id=None
		previous_position=0.0
		max_length=-1.0
		for label in cmap.parse():
			if label.channel != "1":
				continue
			if label.contig_id != current_contig_id:
				current_contig_id=label.contig_id
				previous_position=0.0
			length=label.position-previous_position
			raw_lengths.append(length)
			if length > max_length:
				max_length = length

	with open(raw_lengths_file, 'w') as o_file:
		for raw_length in raw_lengths:
			o_file.write(str(raw_length)+"\t")

	lengths=OrderedDict()
	bin_max=0
	while bin_max < max_length:
		bin_max+=bin_width
		lengths[bin_max]=0

	for raw_length in raw_lengths:
		for bin_max in lengths:
			if raw_length < bin_max:
				lengths[bin_max]+=1
				break

	with open(lengths_file, 'w') as o_file:
		for bin_max in lengths:
			o_file.write(str(bin_max)+"\t"+str(lengths[bin_max])+"\n")

	return lengths

def calculate_ibs(dist_one, dist_two):
	if len(dist_one)>=len(dist_two):
		to_iterate=dist_one
		not_to_iterate=dist_two
	else:
		not_to_iterate=dist_one
		to_iterate=dist_two
	possible=0
	identical=0
	for bin_max in to_iterate:
		if not bin_max in not_to_iterate:
			possible+=to_iterate[bin_max]
			continue
		values=[to_iterate[bin_max], not_to_iterate[bin_max]]
		possible+=max(values)
		identical+=min(values)
	return float(identical)/possible

def format_distance_nex(ibs):
	last_taxa_printed=False
	output=""
	current_taxa_one=""
	for pair_name in sorted(ibs.keys(), reverse=True):
		taxa=pair_name.split("-")
		taxa_one=taxa[0]
		if not last_taxa_printed:
			last_taxa_printed=True
			output=taxa[1]
		if taxa_one != current_taxa_one:
			current_taxa_one=taxa_one
			output+="\n"+taxa_one
		output+="\t"+str(ibs[pair_name])
	print(output)

kmer_distributions={}
with open(argv[1]) as taxa_file:
	for taxa in taxa_file:
		taxa=taxa.strip()
		kmer_distributions[taxa]=calculate_kmer_distribution(taxa, int(argv[2]))

ibs={}
for taxa_one in kmer_distributions:
	for taxa_two in kmer_distributions:
		if taxa_one==taxa_two:
			continue
		pair_name="-".join(sorted([taxa_one,taxa_two]))
		if pair_name in ibs:
			continue
		ibs[pair_name]=calculate_ibs(kmer_distributions[taxa_one], kmer_distributions[taxa_two])

format_distance_nex(ibs)

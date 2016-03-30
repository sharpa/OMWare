#!/usr/bin/python

import argparse
argument_parser=argparse.ArgumentParser(description="")
argument_parser.add_argument('file',help='A .cmap or .xmap file whose statistics will be reported') 
arguments=argument_parser.parse_args()

from Operations.BioNano.files import CmapFile
from Operations.BioNano.files import XmapFile

def cmap_stats(file):
	print("Stats for: " + file)
	lengths={}
	for label in CmapFile(file).parse():
		lengths[label.contig_id]=label.contig_len
	print("Number of contigs: " + str(len(lengths)))

	length=0
	for x in lengths.values():
		length+=x
	print("Total length: " + str(length))

	target=float(length)/2
	total=0
	for x in sorted(lengths.values(), reverse=True):
		total+=x
		if total>=target:
			print("Contig N50: " + str(x))
			break

def xmap_stats(file):
	from numpy import median
	print("Stats for: " + file)
	bloat=0.0
	total_length=0.0
	total_anchor_length=0.0
	proportions=[]
	proportion_count_below_threshold=0
	for align in XmapFile(file).parse():
		length=abs(align.query_start-align.query_end)

		try:
			overhang_length=align.getLeftOverhang().getLength()+align.getRightOverhang().getLength()
			proportion=1-(overhang_length/align.query_len)
			proportions.append(proportion)
			if proportion < 0.9:
				proportion_count_below_threshold+=1
		except:
			proportion_count_below_threshold="unavailable"

		total_length+=length
		bloat+=length*align.confidence

		total_anchor_length+=align.anchor_end-align.anchor_start
	print("Average confidence (weighted): " + str(bloat/total_length))
	if proportion_count_below_threshold!="unavailable":
		median_proportion=median(proportions)
	else:
		median_proportion="unavailable"
	print("Median proportion of BNG contigs in significant alignments: " + str(median_proportion))
	print("Number of BNG contigs less than 90% covered: " + str(proportion_count_below_threshold))
	print("Total length of reference covered: " + str(total_anchor_length))
	print("Total length of assembly covered: " + str(total_length))
	

file=arguments.file
file_name_length=len(file)
print(file[file_name_length-5:file_name_length])
if file[file_name_length-5:file_name_length]==".cmap":
	cmap_stats(file)
else:
	xmap_stats(file)

# Module: Operations.BioNano.Compare.AssessReferenceAlignment
# Version: 0.1
# Author: Aaron Sharp
# Date: 02/29/2016
# 
# The purpose of this module is to assay the disagreements 
# between a BNG map and a reference genome
import os

class AssessReferenceAlignment(object):
	def __init__ (self, xmap_file_name):
		file_name_parts=xmap_file_name.split('/')
		file_name_parts_length=len(file_name_parts)
		self.workspace="/".join(file_name_parts[0:(file_name_parts_length-1)])
		with CD(self.workspace):
			file_name=file_name_parts[file_name_parts_length-1]
			self.xmap=XmapFile(file_name)
			self.anchor_cmap=CmapFile(file_name.replace(".xmap", "_r.cmap"))
			self.query_cmap=CmapFile(file_name.replace(".xmap", "_q.cmap"))

		self.ALIGNED_LABELS=re.compile("\(([\d]+),([\d]+)\)")

	def extractTruePositives(self):
		self.true_positive_labels={}
		self.true_positive_locations={}
		for alignment in self.xmap.parse():
			anchor=alignment.anchor_id
			if not anchor in self.true_positive_labels:
				self.true_positive_labels[anchor]=set()
			if not anchor in self.true_positive_locations:
				self.true_positive_locations[anchor]=[]
			
			for label_pair in self.ALIGNED_LABELS.finditer(alignment.alignment):
				self.true_positive_labels[anchor].add(int(label_pair.group(1)))

		for label in self.anchor_cmap.parse():
			if not label.contig_id in self.true_positive_labels:
				continue
			if label.label_id in self.true_positive_labels[label.contig_id]:
				self.true_positive_locations[label.contig_id].append(label.position)
		return self.true_positive_locations

	def extractFalseNegatives(self):
		# false negative lables are present in the anchor, not in the query
		self.false_negative_labels={}
		self.false_negative_locations={}

		for alignment in self.xmap.parse():
			anchor=alignment.anchor_id
			if not anchor in self.false_negative_labels:
				self.false_negative_labels[anchor]=set()
			if not anchor in self.false_negative_locations:
				self.false_negative_locations[anchor]=[]
			
			previous_label=None
			for label_pair in self.ALIGNED_LABELS.finditer(alignment.alignment):
				anchor_label=int(label_pair.group(1))

				if previous_label is None:
					previous_label=anchor_label
					continue

				for i in xrange(previous_label+1,anchor_label):
					self.false_negative_labels[anchor].add(i)
				previous_label=anchor_label

		for label in self.anchor_cmap.parse():
			if not label.contig_id in self.false_negative_labels:
				continue
			if label.label_id in self.false_negative_labels[label.contig_id]:
				self.false_negative_locations[label.contig_id].append(label.position)
		return self.false_negative_locations

	def extractFalsePositives(self):
		self.false_positive_labels={}
		for alignment in self.xmap.parse():
			anchor=alignment.anchor_id
			query=alignment.query_id
			if not query in self.false_positive_labels:
				self.false_positive_labels[query]={}
			
			previous_label_pair=None
			for label_pair in self.ALIGNED_LABELS.finditer(alignment.alignment):
				if previous_label_pair is None:
					previous_label_pair=label_pair
					continue

				previous_query_label=int(previous_label_pair.group(2))
				query_label=int(label_pair.group(2))

				if alignment.orientation=="+":
					start=previous_query_label+1
					stop=query_label
				else:
					start=query_label+1
					stop=previous_query_label
				for i in xrange(start, stop):
					self.false_positive_labels[query][i]={"anchor_id": anchor, "anchor_last_true_positive": int(previous_label_pair.group(1)), "query_last_true_positive": int(previous_label_pair.group(2))}

				previous_label_pair=label_pair

		false_positive_offsets={}
		last_true_positive=None
		for label in self.query_cmap.parse():
			if not label.contig_id in self.false_positive_labels:
				last_true_positive=label
				continue
			if not label.label_id in self.false_positive_labels[label.contig_id]:
				last_true_positive=label
				continue

			false_positive=self.false_positive_labels[label.contig_id][label.label_id]
			anchor=false_positive["anchor_id"]
			anchor_label=false_positive["anchor_last_true_positive"]
			if not anchor in false_positive_offsets:
				false_positive_offsets[anchor]={}
			if not anchor_label in false_positive_offsets[anchor]:
				false_positive_offsets[anchor][anchor_label]=[]
			
			false_positive_offsets[anchor][anchor_label].append(label.position-last_true_positive.position)

		self.false_positive_locations={}
		for label in self.anchor_cmap.parse():
			if not label.contig_id in false_positive_offsets:
				continue
			if not label.label_id in false_positive_offsets[label.contig_id]:
				continue

			if not label.contig_id in self.false_positive_locations:
				self.false_positive_locations[label.contig_id]=[]
			for offset in false_positive_offsets[label.contig_id][label.label_id]:
				self.false_positive_locations[label.contig_id].append(label.position+offset)

		return self.false_positive_locations

	def extractSequenceContexts(self, loci):
		pass
	def processSeqeuenceContexts(self, fasta_file):
		pass

	def findNearestNeighbors(self,loci,neighbor_locis):
		neighbors={}
		for chr in loci:
			if not chr in neighbors:
				neighbors[chr]=[]
			for locus in loci[chr]:
				nearest_dist=None
				for neighbor_loci in neighbor_locis:
					if not chr in neighbor_loci:
						continue
					for neighbor_locus in neighbor_loci[chr]:
						dist=abs(locus-neighbor_locus)
						if nearest_dist is None or dist<nearest_dist:
							nearest_dist=dist
				if nearest_dist is not None:
					neighbors[chr].append(nearest_dist)
		return neighbors

import re
from Utils.CD import CD
from Operations.BioNano.files import CmapFile
from Operations.BioNano.files import XmapFile
from Operations.BioNano.FileConverter import FastaFile

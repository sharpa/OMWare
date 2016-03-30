# Module: Operations.BioNano.Compare.Comparison
# Version: 0.1
# Author: Aaron Sharp
# Date: 03/18/16
# 
# The purpose of this module is to describe and proces the results
# of any comparison step that generates a .xmap alignment file

class Comparison(object):
	def __init__(self, xmap_file):
		self.xmap_file=xmap_file
		self.query_file, self.anchor_file=self.seekCmaps()

		error=False
		error_message="Unable to find "
		if self.query_file is None:
			error=True
			error_message+="query, "
		if self.anchor_file is None:
			error=True
			error_message+="anchor"
		if error:
			raise FileArrangementException(error_message+" maps.")

	def seekCmaps(self):
		query_file=None
		anchor_file=None
		query_candidates=[self.xmap_file.input_file.replace('.xmap', '_q.cmap')]
		anchor_candidates=[self.xmap_file.input_file.replace('.xmap', '_r.cmap')]
		for header in self.xmap_file.getHeaders():
			if "Query Maps From" in header:
				query_candidates.append(header.split("\t")[1])
			elif "Reference Maps From" in header:
				anchor_candidates.append(header.split("\t")[1])

		for candidate in query_candidates:
			try:
				query_file=CmapFile(candidate)
				break
			except:
				pass
		for candidate in anchor_candidates:
			try:
				anchor_file=CmapFile(candidate)
				break
			except:
				pass
			
		return query_file, anchor_file

	def findBreakPoints(self):
		break_points=[]

		query_contigs=self.query_file.loadContigs()
		anchor_contigs=self.anchor_file.loadContigs()

		for align in self.xmap_file.parse():
			try:
				query_length=align.query_len
			except:
				raise # extract query length from query_file

			try:
				align.anchor=anchor_contigs[align.anchor_id]
			except:
				raise FileMismatchException(self.xmap_file.input_file, self.anchor_file.input_file, align.anchor_id)
			try:
				align.query=query_contigs[align.query_id]
			except:
				raise FileMismatchException(self.xmap_file.input_file, self.query_file.input_file, align.query_id)

			for overhang in [align.getLeftOverhang(), align.getRightOverhang()]:
				proportion=overhang.getLength()/query_length
				if proportion>=0.05:
					overhanging_label_positions=align.getOverhangingLabels(overhang).keys()
					len_overhanging_label_positions=len(overhanging_label_positions)
					if len_overhanging_label_positions > 1:
						end=overhanging_label_positions[1]
					elif len_overhanging_label_positions == 1:
						end=overhanging_label_positions[0]
					else:
						continue
					start=int(overhang.start)
					end=int(end)
					chrom="Chr0" if len(str(align.anchor_id))==1 else "Chr"
					break_points.append([chrom+str(align.anchor_id), min(start, end), max(start, end), align.query_id, align.confidence, overhang.orientation])
				
		return break_points

from Operations.BioNano.files import XmapFile
from Operations.BioNano.files import CmapFile
from Operations.BioNano.exceptions import FileArrangementException
from Operations.BioNano.exceptions import FileMismatchException

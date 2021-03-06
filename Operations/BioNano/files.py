# Module: Operations.BioNano.files
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to manipulate optical maps
# as they appear in a variety of BNG file formats
from collections import OrderedDict

class File(object):
	def __init__(self, input_file):
		i_file=open(input_file, "r")
		i_file.close()
		self.input_file=input_file
	def __eq__(self, other):
		if other is None:
			return False
		return self.input_file==other.input_file
	def __ne__(self, other):
		return self.input_file!=other.input_file

	@staticmethod
	def getExtension():
		raise Exception("Abstract method called")

	def getHeaders(self):
		headers=[]
		with open(self.input_file, "r") as i_file:
			for line in i_file:
				if line[0]=="#":
					headers.append(line.strip())
				else:
					break
		return headers

	def parse(self):
		raise Exception("Abstract method called")
	def write(self, entity, o_file):
		raise Exception("Abstract method called")
	def writeDefaultHeaders(self, o_file):
		raise Exception("Abstract method called")

	def getFileName(self):
		return self.input_file
		
class File_iter(object):
	def __init__(self, input_file):
		self.i_file=open(input_file, "r")
	def __iter__(self):
		return self
	def __eq__(self, other):
		if other is None:
			return False
		if self.__class__ != other.__class__:
			return False
		return self.i_file.name==other.i_file.name
	def __ne__(self, other):
		return not self == other
	def next(self):
		raise Exception("Abstract method called")

class BnxFile(File):
	@staticmethod
	def getExtension():
		return "bnx"

	def parse(self):
		return BnxFile_iter(self.input_file)

	def write(self, molecule, o_file):

		o_file.write("	".join(["0", str(molecule.id), str(molecule.length), str(molecule.average_intensity), str(molecule.snr), str(molecule.num_labels), str(molecule.original_id), str(molecule.scan_id), str(molecule.scan_direction), str(molecule.chip_id), str(molecule.flowcell), str(molecule.run_id), str(molecule.global_scan_id)]) + "\n")

		label_data=["1", "0.0"]
		label_data.extend([str(i) for i in molecule.labels])
		o_file.write("	".join(label_data) + "\n")

		quality_one_data=["QX11"]
		quality_one_data.extend(molecule.qualities_one)
		o_file.write("	".join(quality_one_data) + "\n")

		quality_two_data=["QX12"]
		quality_two_data.extend(molecule.qualities_two)
		o_file.write("	".join(quality_two_data) + "\n")

class BnxFile_iter(File_iter):
	def next(self):
		while True:
			try:
				line=self.i_file.readline()
				if line=='':
					self.i_file.close()
					raise StopIteration

				if line[0]=="#":
					continue

				if line [0] != "0":
					raise Exception("this file is incorrectly formatted")
				molecule_data=line.split()
				new_molecule=Molecule(molecule_data[1], float(molecule_data[2]))

				new_molecule.average_intensity=molecule_data[3]
				new_molecule.snr=molecule_data[4]
				new_molecule.num_labels=molecule_data[5]
				new_molecule.original_id=molecule_data[6]
				new_molecule.scan_id=molecule_data[7]
				new_molecule.scan_direction=molecule_data[8]
				new_molecule.chip_id=molecule_data[9]
				new_molecule.flowcell=molecule_data[10]
				new_molecule.run_id=molecule_data[11]
				new_molecule.global_scan_id=molecule_data[12]

				label_line=self.i_file.readline()
				if label_line[0] != "1":
					raise Exception("this file is incorrectly formatted")
				new_molecule.labels=label_line.split()[2:]
				
				quality_line_one=self.i_file.readline()
				if quality_line_one[0:4] != "QX11":
					raise Exception("this file is incorrectly formatted")
				new_molecule.qualities_one=quality_line_one.split()[1:]
				
				quality_line_two=self.i_file.readline()
				if quality_line_two[0:4] != "QX12":
					raise Exception("this file is incorrectly formatted")
				new_molecule.qualities_two=quality_line_two.split()[1:]

				return new_molecule
			except StopIteration:
				raise
			except IndexError:
				raise Exception("this file is incorrectly formatted")
			except:
				raise


class Molecule:
	def __init__(self, id, length):
		self.id=id
		self.length=length

	def shrink(self, new_length):
		self.length=new_length

		num_labels=len(self.labels)
		last_label_index=-1
		for i in xrange(num_labels-1, -1, -1):
			if float(self.labels[i]) <= float(self.length):
				last_label_index=i
				break
			if i==0:
				last_label_index=0

		quality_one_of_molecule_end=self.qualities_one[num_labels-1]
		quality_two_of_molecule_end=self.qualities_two[num_labels-1]

		self.labels=self.labels[0:last_label_index]
		self.qualities_one=self.qualities_one[0:last_label_index]
		self.qualities_two=self.qualities_two[0:last_label_index]

		self.labels.append(self.length)
		self.qualities_one.append(quality_one_of_molecule_end)
		self.qualities_two.append(quality_two_of_molecule_end)

		self.num_labels=last_label_index+1

class CmapFile(File):
	@staticmethod
	def getExtension():
		return "cmap"
	def parse(self):
		return CmapFile_iter(self.input_file)
	def write(self, label, o_file):
		fields=[str(label.contig_id),
			str(label.contig_len),
			str(label.contig_site_count),
			str(label.label_id),
			label.channel,
			str(label.position),
			str(label.stdev),
			str(label.coverage),
			str(label.occurrences)]
		if hasattr(label, 'snr_mean'):
			fields.extend([str(label.snr_mean),
				str(label.snr_stdev),
				str(label.snr_count)])
		o_file.write("\t".join(fields) + "\n")
	def writeDefaultHeaders(self, o_file):
		o_file.write("""# CMAP File Version:    0.1
# Label Channels:       1
# Nickase Recognition Site 1:   cctcagc
# Enzyme1:      Nt.BbvCI
#h CMapId       ContigLength    NumSites        SiteID  LabelChannel    Positio
#f int  float   int     int     int     float   float   int     int\n""")
	def loadContigs(self):
		contigs={}
		final_labels={}
		for label in self.parse():
			if not label.contig_id in contigs:
				contigs[label.contig_id]=Contig()
			contigs[label.contig_id].addLabel(label, sort=False)

			final_labels[label.contig_id]=label

		for contig_id in final_labels.keys():
			contigs[contig_id].addLabel(final_labels[contig_id], sort=True)

		return contigs

class CmapFile_iter(File_iter):
	def next(self):
		while True:
			try:
				line=self.i_file.readline()
				if line=='':
					self.i_file.close()
					raise StopIteration
				if line[0]=="#":
					continue
				label_data=line.split("\t")
				# The cmap file format may have 9, 11 or 12 fields, depending on if it is in silico digested, unmerged, or merged respectively
				if len(label_data)<9:
					raise Exception("this file is incorrectly formatted")

				label_id=int(label_data[3])
				contig_id=int(label_data[0])
				new_label=Label(contig_id, label_id)

				new_label.contig_len=float(label_data[1])
				new_label.contig_site_count=int(label_data[2])

				new_label.channel=label_data[4]
				new_label.position=float(label_data[5])
				new_label.stdev=float(label_data[6])
				new_label.coverage=float(label_data[7]) # I'm not sure why this is a float, not an int
				new_label.occurrences=float(label_data[8])
				if len(label_data) > 9:
					new_label.snr_mean=float(label_data[9])
					new_label.snr_stdev=float(label_data[10])
				if len(label_data) > 11:
					new_label.snr_count=float(label_data[11])
				
				return new_label

			except StopIteration:
				raise
			except IndexError:
				raise Exception("this file is incorrectly formatted")
			except:
				raise
				
class Label:
	def __eq__(self, other):
		if other is None:
			return False
		return self.__dict__ == other.__dict__
	def __init__(self, contig_id, label_id):
		self.contig_id=contig_id
		self.label_id=label_id

class Contig(object):
	def __init__(self):
		self.unordered_labels={}
		self.labels=OrderedDict()
	def addLabel(self, label, sort=True, reverse=False):
		self.unordered_labels[label.position]=label

		if sort:
			self.labels=OrderedDict()
			for position in sorted(self.unordered_labels.keys(), reverse=reverse):
				self.labels[position]=self.unordered_labels[position]
		else:
			self.labels[label.position]=label

class XmapFile(File):
	@staticmethod
	def getExtension():
		return "xmap"

	def parse(self):
		return XmapFile_iter(self.input_file)
	def write(self, alignment, o_file):
		fields=[str(alignment.alignment_id),
			str(alignment.query_id),
			str(alignment.anchor_id),
			str(alignment.query_start),
			str(alignment.query_end),
			str(alignment.anchor_start),
			str(alignment.anchor_end),
			alignment.orientation,
			str(alignment.confidence),
			alignment.hit_enum,
			str(alignment.query_len),
			str(alignment.anchor_len),
			alignment.label_channel,
			alignment.alignment
			]
		o_file.write("\t".join(fields) + "\n")
		
class XmapFile_iter(File_iter):
	line_number=0
	def next(self):
		while True:
			self.line_number+=1
			try:
				line=self.i_file.readline()
				if line=='':
					self.i_file.close()
					raise StopIteration
				if line[0]=="#":
					continue
				alignment_data=line.strip().split("\t")
				if len(alignment_data)<14:
					raise Exception("this file is incorrectly formatted (see line {0:d})".format(self.line_number))

				alignment_id=int(alignment_data[0])
				query_id=int(alignment_data[1])
				anchor_id=int(alignment_data[2])
				new_alignment=Alignment(alignment_id, query_id, anchor_id)

				new_alignment.query_start=float(alignment_data[3])
				new_alignment.query_end=float(alignment_data[4])
				new_alignment.query_len=float(alignment_data[10])
				new_alignment.anchor_start=float(alignment_data[5])
				new_alignment.anchor_end=float(alignment_data[6])
				new_alignment.anchor_len=float(alignment_data[11])

				new_alignment.orientation=alignment_data[7]
				new_alignment.confidence=float(alignment_data[8])
				new_alignment.hit_enum=alignment_data[9]
				new_alignment.label_channel=alignment_data[12]
				new_alignment.alignment=alignment_data[13]

				return new_alignment

			except StopIteration:
				raise
			except IndexError:
				raise Exception("this file is incorrectly formatted (see line {0:d})".format(self.line_number))
			except:
				raise
class Alignment:
	def __eq__(self, other):
		if other is None:
			return False
		return self.__dict__ == other.__dict__
	def __init__(self, alignment_id, query_id, anchor_id):
		self.alignment_id=alignment_id
		self.query_id=query_id
		self.anchor_id=anchor_id
	def __repr__(self):
		return str(self.__dict__)

	def getLeftOverhang(self):
		try:
			return self.left_overhang
		except:
			pass

		try:
			query_len=self.query_len
			anchor_len=self.anchor_len
		except:
			raise # extract query length from cmap_file?

		left_start=self.anchor_start
		if self.orientation=='+':
			left_end=self.anchor_start-self.query_start
		else:
			left_end=self.anchor_start-(query_len-self.query_start)

		self.left_overhang=Overhang(left_start, left_end, '-', anchor_len)
		return self.left_overhang

	def getRightOverhang(self):
		try:
			return self.right_overhang
		except:
			pass
		try:
			query_len=self.query_len
			anchor_len=self.anchor_len
		except:
			raise # extract query length from cmap_file?

		right_start=self.anchor_end
		if self.orientation=='+':
			right_end=self.anchor_end+(query_len-self.query_end)
		else:
			right_end=self.anchor_end+self.query_end

		self.right_overhang=Overhang(right_start, right_end, '+', anchor_len)
		return self.right_overhang

	def getOverhangingLabels(self, overhang):
		if not self.query or not self.anchor or not self.query_len or not self.anchor_len:
			raise Exception("Illegal state: Cannot find overhanging labels without query or anchor contigs, or without query_len")

		if overhang.orientation=="+":
			start=overhang.start
			end=overhang.end
		else:
			start=overhang.end
			end=overhang.start
		unordered_overhanging_labels={}
		#remove .labels by adding __getitem__ to Contig class
		for label_position in self.anchor.labels.keys():
			if label_position>start and label_position<end:
				unordered_overhanging_labels[label_position]=self.anchor.labels[label_position]

		#if left overhang
		if overhang.orientation=='-':
			query_offsets={}
			if self.orientation=='-':
				#find labels between query_len and query_start
				for label_position in self.query.labels.keys():
					if label_position>self.query_len and label_position<self.query_start:
						query_offsets[label_position-self.query_start]=self.query.labels[label_position]
			else:
				#find labels between zero and query_start
				for label_position in self.query.labels.keys():
					if label_position>0 and label_position<self.query_start:
						query_offsets[self.query_start-label_position]=self.query.labels[label_position]

			#convert to anchor position: anchor_start-distance
			for query_offset in query_offsets.keys():
				anchor_position=self.anchor_start-query_offset
				unordered_overhanging_labels[anchor_position]=query_offsets[query_offset]
			
		#if right overhang
		else:
			query_offsets={}
			if self.orientation=='-':
				#find labels between query_end and 0
				for query_position in self.query.labels.keys():
					if query_position<self.query_end and query_position>0:
						query_offsets[self.query_end-query_position]=self.query.labels[query_position]
			else:
				#find labels between query_end and query_len
				for query_position in self.query.labels.keys():
					if query_position>self.query_end and query_position<self.query_len:
						query_offsets[query_position-self.query_end]=self.query.labels[query_position]

			# convert to anchor position: anchor_end+distance
			for query_offset in query_offsets.keys():
				anchor_position=self.anchor_end+query_offset
				unordered_overhanging_labels[anchor_position]=query_offsets[query_offset]

		reverse=overhang.orientation=='-'
		overhanging_labels=OrderedDict()
		for label_position in sorted(unordered_overhanging_labels.keys(), reverse=reverse):
			if label_position<0 or label_position>self.anchor_len:
				continue
			overhanging_labels[label_position]=unordered_overhanging_labels[label_position]
		return overhanging_labels
		
		

class Overhang(object):
	def __init__(self, start, end, orientation, anchor_len):
		self.anchor_len=anchor_len
		self.start=start
		self.orientation=orientation
		if orientation=='-':
			if end < 0:
				end=0
		if orientation=='+':
			if end > anchor_len:
				end=anchor_len
		self.end=end
	def __repr__(self):
		return str(self.__dict__)
	def getLength(self):
		return abs(self.end-self.start)

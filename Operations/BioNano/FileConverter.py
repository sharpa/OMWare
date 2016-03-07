#!/fslhome/jtpage/bin/python 
import sys

class FileConverter:
	def __init__(self, input_file, output_file=None):
		self.input_file=input_file
		self.output_file=output_file

		self.digestor=None

	def convert(self):
		if self.output_file is None:
			raise Exception("Can't convert without target file format info")

		# This is poorly designed
		if self.input_file.getExtension()=="fa":
			if self.output_file.getExtension()=="cmap":
				self.convert_from_fasta_to_cmap()
		elif self.input_file.getExtension()=="xmap":
			if self.output_file.getExtension()=="bed":
				self.convert_from_xmap_to_bed()
			elif self.output_file.getExtension()=="sam":
				self.convert_from_xmap_to_sam()
		elif self.input_file.getExtension()=="cmap":
			if self.output_file.getExtension()=="len":
				self.convert_from_cmap_to_len()

	def convert_from_fasta_to_cmap(self):
		if self.digestor is None:
			raise Exception("Can't convert from fasta to cmap without a motif")
		o_file=open(self.output_file.input_file, 'w')
		self.output_file.writeDefaultHeaders(o_file)
		for i, record in enumerate(self.input_file.parse()):
			try:
				contig_id=int(re.sub('[\D]+', '', record.name))
			except:
				contig_id=i
			length=len(record.seq)
			num_ns=len(re.split('N', str(record.seq)))
			prop_ns='{0:.2f}'.format(float(num_ns)/length)
			if length > 2030:
				if float(prop_ns) < .1:
					labels=self.digestor.digest(record, contig_id)
					for label in labels:
						self.output_file.write(label, o_file)

	def convert_from_xmap_to_bed(self):
		with open(self.output_file.input_file, 'w') as o_file:
			self.output_file.writeDefaultHeaders(o_file)
			for i, alignment in enumerate(self.input_file.parse()):
				chrom="chr"+str(alignment.anchor_id)
				if alignment.orientation=="+":
					start=alignment.anchor_start-alignment.query_start
					stop=alignment.anchor_end+(alignment.query_len-alignment.query_end)
				elif alignment.orientation=="-":
					start=alignment.anchor_start-(alignment.query_len-alignment.query_end)
					stop=alignment.anchor_end+alignment.query_start
				if start < 0:
					start=0
				if stop > alignment.anchor_len:
					stop=alignment.anchor_len
				name="contig"+str(alignment.query_id)
				feature=Feature(chrom, int(start), int(stop), name)
				feature.score=int(alignment.confidence*10)
				feature.strand=alignment.orientation
				feature.thick_start=int(alignment.anchor_start)
				feature.thick_end=int(alignment.anchor_end)
				feature.item_rgb=[0,0,0]
				feature.block_count=0
				feature.block_sizes=[0]
				feature.block_starts=[0]
				
				self.output_file.write(feature,o_file)

	def convert_from_xmap_to_sam(self):
		anchors={}
		confidence_maxima={}
		for align in self.input_file.parse():
			anchors[align.anchor_id]=align.anchor_len

			if not align.query_id in confidence_maxima:
				confidence_maxima[align.query_id]=align.confidence
			elif align.confidence > confidence_maxima[align.query_id]:
				confidence_maxima[align.query_id]=align.confidence

		with open(self.output_file.input_file, 'w') as o_file:
			o_file.write("@HD\tVN:1.0\tSO:unsorted\n")
			for anchor in sorted(anchors.keys()):
				o_file.write("@SQ\tSN:"+str(anchor)+"\tLN:"+str(int(anchors[anchor]))+"\n")

			for align in self.input_file.parse():
				flag=0
				if align.orientation=="-":
					flag+=16
				if align.confidence!=confidence_maxima[align.query_id]:
					flag+=256
				start_pos=align.anchor_start
				if start_pos==0:
					start_pos=1
				output=[
					str(align.query_id),
					str(flag),
					str(align.anchor_id),
					str(int(start_pos)),
					str(int(align.confidence)),
					align.hit_enum.replace('M','='),
					"*","0",
					str(int(align.query_len)),
					"*","*"
				]
				o_file.write("\t".join(output)+"\n")

	def convert_from_cmap_to_len(self):
		with open(self.output_file.input_file, 'w') as o_file:
			ids=set()
			for i, label in enumerate(self.input_file.parse()):
				if label.contig_id in ids:
					continue
				ids.add(label.contig_id)
				name="chr"+str(label.contig_id)
				length=int(label.contig_len)
				chromosome=Chromosome(name, length)
				self.output_file.write(chromosome,o_file)
		
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
from files import Label
import re
class Digestor(object):
	def __init__(self, motif):
		upper_motif=motif.upper()
		self.motif=Seq(upper_motif,generic_dna)
		self.rev_motif=self.motif.reverse_complement()
	def digest(self, seqRecord, contig_id=1):
		chromosome = seqRecord.seq.upper()
		fragments=[]
		forward_fragments=re.split(str(self.motif), str(chromosome))
		for fragment in forward_fragments:
			fragments.extend(re.split(str(self.rev_motif), str(fragment)))
		try:
			while(True):
				fragments.remove("")
		except:
			pass
		length = len(chromosome)
		count = len(fragments)

		position=0
		labels=[]
		if count > 1:
			for i, fragment in enumerate(fragments):
				label_id=i+1
				label=Label(contig_id, label_id)
				label.contig_len=length
				label.contig_site_count=count
				label.channel="1"
				position+=len(fragment)
				label.position=position
				label.stdev=1.0
				label.coverage=1
				label.occurrences=1
				labels.append(label)
			label=Label(contig_id, count+1)
			label.contig_len=length
			label.contig_site_count=count
			label.channel="0"
			label.position=length
			label.stdev=0.0
			label.coverage=1
			label.occurrences=0
			labels.append(label)
		return labels
			

from files import File
from files import File_iter
from Bio import SeqIO
class FastaFile(File):
	@staticmethod
	def getExtension():
		return "fa"

	def parse(self):
		return SeqIO.parse(open(self.input_file), 'fasta')
	def write(self, entity, o_file):
		SeqIO.write(entity, o_file, 'fasta')

class BedFile(File):
	@staticmethod
	def getExtension():
		return "bed"

	def getHeaders(self):
		headers=[]
		with open(self.input_file, 'r') as i_file:
			for line in i_file:
				fields=line.split("\t")
				if len(fields) < 12:
					headers.append(line)
				else:
					break
		return headers

	def parse(self):
		return BedFile_iter(self.input_file)
	def write(self, feature, o_file):
		fields=[feature.chrom,
			str(feature.start),
			str(feature.stop),
			feature.name,
			str(feature.score),
			feature.strand,
			str(feature.thick_start),
			str(feature.thick_end),
			",".join([str(x) for x in feature.item_rgb]),
			str(feature.block_count),
			",".join([str(x) for x in feature.block_sizes]),
			",".join([str(x) for x in feature.block_starts])]
		o_file.write("\t".join(fields)+"\n")

	def writeDefaultHeaders(self, o_file):
		o_file.write("track name=custom_track description=\"Default description\" useScore=1\n")
		o_file.write("itemRgb=\"On\"\n")

class BedFile_iter(File_iter):
	def next(self):
		while True:
			try:
				line=self.i_file.readline()
				if line=='':
					self.i_file.close()
					raise StopIteration
				feature_data=line.split("\t")
				if len(feature_data) < 12:
					continue
				chrom=feature_data[0]
				start=int(feature_data[1])
				stop=int(feature_data[2])
				name=feature_data[3]
				feature=Feature(chrom, start, stop, name)
				feature.score=int(feature_data[4])
				feature.strand=feature_data[5]
				feature.thick_start=int(feature_data[6])
				feature.thick_end=int(feature_data[7])
				feature.item_rgb=[int(x) for x in feature_data[8].split(',')]
				feature.block_count=int(feature_data[9])
				feature.block_sizes=[int(x) for x in feature_data[10].split(',')]
				feature.block_starts=[int(x) for x in feature_data[11].split(',')]
				return feature
			except StopIteration:
				raise
			except IndexError:
				raise Exception("this file is incorrectly formatted")
			except:
				raise
				
class Feature(object):
	def __init__(self, chrom, start, stop, name):
		self.chrom=chrom
		self.start=start
		self.stop=stop
		self.name=name

class LenFile(File):
	@staticmethod
	def getExtension():
		return "len"

	def parse(self):
		return LenFile_iter(self.input_file)
	def write(self, chromosome, o_file):
		fields=[chromosome.name,
			str(chromosome.length)]
		o_file.write("\t".join(fields)+"\n")

	def writeDefaultHeaders(self, o_file):
		pass

class LenFile_iter(File_iter):
	def next(self):
		while True:
			try:
				line=self.i_file.readline()
				if line=='':
					self.i_file.close()
					raise StopIteration
				if line[0]=="#":
					continue
				chromosome_data=line.split("\t")
				name=chromosome_data[0]
				length=int(chromosome_data[1])
				chromosome=Chromosome(name, length)
				return chromosome
			except StopIteration:
				raise
			except IndexError:
				raise Exception("this file is incorrectly formatted")
			except:
				raise
				
class Chromosome(object):
	def __init__(self, name, length):
		self.name=name
		self.length=length

class SamFile(File):
	def __iter__(self):
		raise Exception("This feature not implemented for sam files")

	@staticmethod
	def getExtension():
		return "sam"

	def parse(self):
		raise Exception("This feature not implemented for sam files")
	
	def next(self):
		raise Exception("This feature not implemented for sam files")

	def write(self, alignment, o_file):
		pass

	def writeDefaultHeaders(self, o_file):
		raise Exception("This feature not implemented for sam files")

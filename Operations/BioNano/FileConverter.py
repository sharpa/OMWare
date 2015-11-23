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

		if self.input_file.getExtension()=="fa":
			if self.output_file.getExtension()=="cmap":
				self.convert_from_fasta_to_cmap()

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
from Bio import SeqIO
class FastaFile(File):
	@staticmethod
	def getExtension():
		return "fa"

	def parse(self):
		return SeqIO.parse(open(self.input_file), 'fasta')
	def write(self, entity, o_file):
		SeqIO.write(entity, o_file, 'fasta')

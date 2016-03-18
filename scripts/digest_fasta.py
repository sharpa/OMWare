#!/usr/bin/python

from sys import argv
from Operations.BioNano.FileConverter import FileConverter
from Operations.BioNano.FileConverter import FastaFile
from Operations.BioNano.FileConverter import Digestor
from Operations.BioNano.files import CmapFile
from Bio import SeqIO

if len(argv) < 4:
	print("USAGE: python digest_fasta.py input_file.fasta MOTIF output_file.cmap")
	exit(1)

conv=FileConverter(FastaFile(argv[1]))
conv.digestor=Digestor(argv[2])
with open(argv[3], 'w'):
	pass
conv.output_file=(CmapFile(argv[3]))
conv.convert()

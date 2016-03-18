#!/usr/bin/python

import argparse
parser=argparse.ArgumentParser(description='Convert a sequence-based fasta file into a .cmap physical map format by locating (restriction endonuclease) sequence motifs')
parser.add_argument('fasta_file', help='The sequence .fasta file to be converted')
parser.add_argument('motif', help='The sequence motif to locate, e.g. ATCGGCTA. Case does not matter.')
parser.add_argument('cmap_file', help='Name for output .cmap file')
args=parser.parse_args()

from Operations.BioNano.FileConverter import FileConverter
from Operations.BioNano.FileConverter import FastaFile
from Operations.BioNano.FileConverter import Digestor
from Operations.BioNano.files import CmapFile
from Bio import SeqIO

conv=FileConverter(FastaFile(args.fasta_file))
conv.digestor=Digestor(args.motif)
with open(args.cmap_file, 'w'):
	pass
conv.output_file=(CmapFile(args.cmap_file))
conv.convert()

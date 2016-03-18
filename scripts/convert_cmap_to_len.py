#!/usr/bin/python

import argparse
parser=argparse.ArgumentParser(description='Convert a .cmap reference genome file into a .len file (for example, for viewing on a genome browser)')
parser.add_argument('cmap_file', help='A .cmap file whose contigs will be turned into lengths')
args=parser.parse_args()

from Operations.BioNano.files import CmapFile
from Operations.BioNano.FileConverter import FileConverter
from Operations.BioNano.FileConverter import LenFile

cmap_path=args.cmap_file
len_path=cmap_path.replace(".cmap",".len")
with open(len_path,'w'):
	pass
len_file_converter=FileConverter(CmapFile(cmap_path), LenFile(len_path))
len_file_converter.convert()

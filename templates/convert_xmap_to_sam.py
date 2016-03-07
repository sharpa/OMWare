#!/usr/bin/python

from sys import argv
if len(argv)<2:
	print("USAGE: python convert_xmap_to_sam.py <input.xmap>")
	exit(1)

from Operations.BioNano.FileConverter import FileConverter
from Operations.BioNano.FileConverter import SamFile
from Operations.BioNano.files import XmapFile

xmap_path=argv[1]
xmap=XmapFile(xmap_path)
sam_path=xmap_path.replace('.xmap', '.sam')
with open(sam_path, 'w'):
	sam=SamFile(sam_path)

fc=FileConverter(xmap, sam)
fc.convert()

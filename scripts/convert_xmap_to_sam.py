#!/usr/bin/python

import argparse
parser=argparse.ArgumentParser(description='Convert a .xmap alignment file into a .sam (Sequence Alignment/Map Format) file.')
parser.add_argument('xmap_file', help='.xmap file to be converted')
args=parser.parse_args()

from Operations.BioNano.FileConverter import FileConverter
from Operations.BioNano.FileConverter import SamFile
from Operations.BioNano.files import XmapFile

xmap_path=args.xmap_file
xmap=XmapFile(xmap_path)
sam_path=xmap_path.replace('.xmap', '.sam')
with open(sam_path, 'w'):
	sam=SamFile(sam_path)

fc=FileConverter(xmap, sam)
fc.convert()

#!/usr/bin/python

import argparse
parser=argparse.ArgumentParser(description='Convert a .xmap alignment file into a .bed file, where queries are described as regions of the anchor. You may need to create a .len file as well in order to visualize this alignmetn on a genome browswer (see convert_cmap_to_len.py)')
parser.add_argument('xmap_file', help='A .xmap alignment file, generated such that your "reference" is the anchor')
args=parser.parse_args()

from Operations.BioNano.files import XmapFile
from Operations.BioNano.FileConverter import FileConverter
from Operations.BioNano.FileConverter import BedFile

xmap_path=args.xmap_file
bed_path=xmap_path.replace(".xmap",".bed")
with open(bed_path,'w'):
	pass

bed_file_converter=FileConverter(XmapFile(xmap_path), BedFile(bed_path))
bed_file_converter.convert()

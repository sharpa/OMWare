#!/fslhome/jtpage/bin/python

from sys import argv
if len(argv)<2:
	print("USAGE: python convert_xmap_to_bed.py <input.xmap>")
	exit(1)

from Operations.BioNano.files import XmapFile
from Operations.BioNano.FileConverter import FileConverter
from Operations.BioNano.FileConverter import BedFile

xmap_path=argv[1]
bed_path=xmap_path.replace(".xmap",".bed")
with open(bed_path,'w'):
	pass

bed_file_converter=FileConverter(XmapFile(xmap_path), BedFile(bed_path))
bed_file_converter.convert()

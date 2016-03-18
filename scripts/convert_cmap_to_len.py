#!/fslhome/jtpage/bin/python

from sys import argv
if len(argv) < 2:
	print("USAGE: python convert_cmap_len.py <input.cmap>")
	exit(1)

from Operations.BioNano.files import CmapFile
from Operations.BioNano.FileConverter import FileConverter
from Operations.BioNano.FileConverter import LenFile

cmap_path=argv[1]
len_path=cmap_path.replace(".cmap",".len")
with open(len_path,'w'):
	pass
len_file_converter=FileConverter(CmapFile(cmap_path), LenFile(len_path))
len_file_converter.convert()

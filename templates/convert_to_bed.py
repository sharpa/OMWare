#!/usr/bin/python

from Operations.BioNano.Compare.ReferenceAlignment import ReferenceAlignment
from Operations.BioNano.Assemble.Merge import Merge
from Operations.BioNano.Assemble.VitalParameters import VitalParameters
from Utils.Workspace import Workspace
from Utils.CD import CD
from Operations.BioNano.files import XmapFile
from Operations.BioNano.FileConverter import BedFile
from Operations.BioNano.FileConverter import LenFile
from Operations.BioNano.files import CmapFile
from Operations.BioNano.FileConverter import FileConverter

work_dir="/path/to/work/dir" ### SET ME
input_file="input.bnx" ### SET ME
workspace=Workspace(work_dir, input_file)

ref_file="reference.cmap" ### SET ME

false_positive=0.5 ### SET ME
false_negative=0.15 ### SET ME
genome_size_mb=900 ### SET ME
p_val=1e-05/genome_size_mb
min_len=100 ### SET ME
min_sites=6 ### SET ME

vital_parameters=VitalParameters(false_positive, false_negative, p_val, min_len, min_sites)
merge=Merge(workspace, vital_parameters)

alignment=ReferenceAlignment(workspace, merge, ref_file)

with CD(work_dir):
	len_file_path=alignment.anchor.getStepDir()+"/"+alignment.output_prefix+".len"
	with open(len_file_path,'w'):
	len_file_converter=FileConverter(CmapFile(alignment.anchor.getOutputFile()), LenFile(len_file_path))
	len_file_converter.convert()

        bed_file_path=alignment.getStepDir()+"/"+alignment.output_prefix+".bed"
	with open(bed_file_path,'w'):
		pass
	bed_file_converter=FileConverter(XmapFile(alignment.getOutputFile()), BedFile(bed_file_path))
	bed_file_converter.convert()

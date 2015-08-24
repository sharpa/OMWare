#!/usr/bin/python

# The purpose of this script is to compare an already completed assembly to a reference genome

from Operations.BioNano.Compare.ReferenceAlignment import ReferenceAlignment
from Operations.BioNano.Assemble.Merge import Merge
from Operations.BioNano.Assemble.Assembly import Assembly
from Operations.BioNano.Assemble.VitalParameters import VitalParameters
from Utils.Workspace import Workspace
from Utils.CD import CD
from Operations.SBATCHCodeFormatter import CodeFormatter

work_dir="/path/to/work/dir/" ### SET ME
reference_file="input_file.cmap" ### SET ME
workspace=Workspace(work_dir, reference_file)
workspace.errorNotificationEmail='address@domain.com' ### SET ME
workspace.addBinary("bng_assembler", "/path/to/Assembler") ### SET ME
workspace.addBinary("bng_ref_aligner", "/path/to/RefAligner") ### SET ME

false_positives=1.5 ### SET ME
false_negatives=.386 ### SET ME
p_val_cutoff=1.11e-6 ### SET ME
min_molecule_len=100 ### SET ME
min_molecule_sites=10 ### SET ME

vital_parameters=VitalParameters(false_positives, false_negatives, p_val_cutoff, min_molecule_len, min_molecule_sites)

with CD(work_dir):
	assembly=Assembly(workspace, vital_parameters) ### SET ME: see options below
	### RefineB1, RefineA, Assembly
	merge=Merge(workspace, assembly)

	step=ReferenceAligment(workspace, merge.getOutputFile())

	formatter=CodeFormatter()
	formatter.runOneStep(step)

#!/usr/local/bin/bash

# The purpose of this script is to select the best assembly from an automated param search
#python -c ' ### UNCOMMENT ME LAST
from Operations.BioNano.Parameterize.ParameterSearch import ParameterSearch
from Utils.Workspace import Workspace
from Utils.CD import CD

work_dir="/path/to/work/dir/" ### SET ME
input_file="input_file.bnx" ### SET ME
workspace=Workspace(work_dir, input_file)

genome_size_mb=900 ### SET ME
parameter_search=ParameterSearch(workspace, genome_size_mb)

#average_label_density=7.0 ### SET ME MAYBE
#expected_label_density=13.5 ### SET ME MAYBE
#parameter_search.optimizeFalsehoods(average_label_density, expected_label_density) ### UNCOMMENT ME MAYBE

with CD(work_dir):
	if not parameter_search.isComplete():
		print("Parameter search is not complete yet, please try back later")
	else:
		quality_report=parameter_search.loadQualityReport(1)
		for item in quality_report:
			print(item)
#' > Quality.txt ### UNCOMMENT ME LAST

if [ ! -e rank_assemblies.R ]
then
	cp /path/to/templates/rank_assemblies.R . ### SET ME
	vim rank_assemblies.R
fi
./rank_assemblies.R

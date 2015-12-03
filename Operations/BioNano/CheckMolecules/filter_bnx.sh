#!/usr/local/bin/bash

if [[ "$3" == "" ]]
then
  echo "USAGE: ./filter_bnx.sh <input.bnx> <molecule_ids.txt> <output_prefix>"
  exit 1
fi

input_bnx=$1
id_file=$2
output_prefix=$3
output=`echo $id_file | sed 's/.*\///' | sed 's/\..*//'`
/fslhome/sharpa/apps/BioNanoTools/RefAligner -i $1 -merge -selectidf $id_file -bnx -o $output_prefix/$output -f -stdout -stderr

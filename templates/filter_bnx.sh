#!/bin/bash

if [[ "$2" == "" ]]
then
  echo "USAGE: ./filter_bnx.sh <input.bnx> <minimum_length_in_kb>"
  exit 1
fi

ref_aligner="/fslgroup/fslg_bionano/compute/refined_assemblies/tools/RefAligner" ### SET ME

if [[ "$3" == "" ]]
then
  output_prefix=`echo "$1" | sed 's/\.bnx$//'`_above"$2"kb
else
  output_prefix="$3"
fi

$ref_aligner -i "$1" -merge -minlen "$2" -bnx -o "$output_prefix" -f -stdout -stderr

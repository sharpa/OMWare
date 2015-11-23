#!/usr/local/bin/bash
if [[ "$2" == "" ]]
then
  echo "USAGE: ./get_unrefined_assembly_stats.sh <assembly_dir> <input_bnx_file>"
  exit 1
fi

dir=$1
for file in $dir/*cmap; do grep -v "^#" $file | head -n 1; done | awk 'BEGIN {assembly_len=0} {assembly_len+=$2} END {print assembly_len}'
ls $dir/*cmap | wc -l
echo ""
bnx_file=$2
grep "^0" $bnx_file | awk 'BEGIN {input_len=0; count=0} {input_len+=$3; count+=1} END {print input_len; print ""; print count}'
grep nummaps $dir/exp_unrefined.contigs | awk -F "=" 'BEGIN {molecs=0; contigs=0} {molecs+=$NF; contigs+=1} END {print molecs/contigs; print molecs}'

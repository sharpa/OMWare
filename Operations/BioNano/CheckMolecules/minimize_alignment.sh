#!/usr/local/bin/bash
#SBATCH --time=12:00:00
#SBATCH --mem=6144M

if [[ "$2" == "" ]]
then
  echo "USAGE: ./minimize_alignment.sh <file_w_list_of_align_files> <min_log10pval>"
  exit 1
fi

cat $1 | while read file
do
  grep "^>" $file | awk '($9>'$2'){print $3"\t"$4"\t"$9}'
done

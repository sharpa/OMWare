#!/usr/local/bin/bash

root="/path/to/OMWare(POMM)/" ### SET ME
# try 'echo $PYTHONPATH' if you're having trouble finding this
output_dir="filtering" ### SET ME
# filtering is a perfectly fine default, but you can call it what you like
input_bnx="/path/to/Input.bnx" ### SET ME
# The .. just means the file can be wherever, relative to the file you're currently in
align_file_list="/path/to/align.list" ### SET ME
# If you're coming from a parameter search, look in a directory "pairwise_input.bnx_fp.../align.list
minlen=100 ### SET ME
# Probably take this from your best assembly in your parameters search
minsites=6 ### SET ME
# Probably take this from your best assembly in your parameters search
minlog10pval=8 ### SET ME
# If the p-value that BioNano recommends for my species is ~1e-8 (genome size in MB / 1e-5), then 8 is a reasonable value here.
email='address@domain.com' ###SET ME

# Set up workspace
if [ ! -d $output_dir ]
then
  mkdir $output_dir
fi

# Extract molecule length and site count statistics
if [ ! -e $output_dir/mol_stats.txt ]
then
  python $root/Operations/BioNano/CheckMolecules/get_mol_stats.py $input_bnx > $output_dir/mol_stats.txt
fi

# Filter molecules based on length and site count
if [ ! -e $output_dir/prefiltered_ids.txt ]
then
  python $root/Operations/BioNano/CheckMolecules/prefilter.py $minlen $minsites $output_dir/mol_stats.txt > $output_dir/prefiltered_ids.txt
fi

# Extract molecule hit stats
if [ ! -e $output_dir/minimized_align.txt ]
then
  $root/Operations/BioNano/CheckMolecules/minimize_alignment.sh $align_file_list $minlog10pval > $output_dir/minimized_align.txt
  # sbatch --mail-type=END --mail-user=$email -o "$output_dir/minimized_align.txt" $root/Operations/BioNano/CheckMolecules/minimize_alignment.sh $align_file_list $minlog10pval ### Uncomment me maybe
  # echo "Re-run filter_troublesome_molecules.sh after sbatch job completes (you will recieve an email)" ### Uncomment me maybe
  # exit 1 ### Uncomment me maybe
fi

# Extract alignment stats
if [ ! -e $output_dir/align_stats.txt ]
then
  python $root/Operations/BioNano/CheckMolecules/get_mol_align_stats.py $output_dir/minimized_align.txt $output_dir/mol_stats.txt $output_dir/prefiltered_ids.txt > $output_dir/align_stats.txt
fi

# Calculate linear regression
if [ ! -e $output_dir/slope_info.txt ]
then
  R --vanilla -f $root/Operations/BioNano/CheckMolecules/calculate_equation.R > $output_dir/slope_info.txt
fi
intercept=`tail -n 2 $output_dir/slope_info.txt | head -n 1 | awk '{print $1}'`
slope=`tail -n 2 $output_dir/slope_info.txt | head -n 1 | awk '{print $2}'`

# Examine the effect of width on coverage
python $root/Operations/BioNano/CheckMolecules/determine_reasonable_width.py $output_dir/align_stats.txt $slope $intercept
echo "Width	Total length (bp)"
echo "What width would you like to use?"
read width

# Get list of molecules ids within expected range
python $root/Operations/BioNano/CheckMolecules/filter.py $output_dir/align_stats.txt $width $slope $intercept > $output_dir/filtered_ids.txt

# Create a filtered BNX file
$root/Operations/BioNano/CheckMolecules/filter_bnx.sh $input_bnx $output_dir/filtered_ids.txt $output_dir

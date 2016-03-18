#!/bin/bash

if [[ "$2" == "" ]]
then
  echo "USAGE: ./merge_bnx.sh <output_prefix> <input1.bnx> [input2.bnx ...]"
  exit 1
fi

output=$1
shift

input=""
for arg in "$@"
do
  input=$input" -i "$arg
done

/fslhome/sharpa/apps/BioNanoTools/RefAligner $input -o $output -stdout -stderr -merge -bnx -minlen 100 -minsites 6 -MaxIntensity 0.6 -maxmem 1 -maxthreads 1

exit 0
# Other options I might want to include
              Only options -mres, -bpp, 
-bppadjust <0/1> : If != 0 : Apply -minlen and -maxlen AFTER performing -bpp adjustment (instead of BEFORE) [Default 1]
-minSNR <V> ... : Remove all -i input map sites with SNR below V (There is One V value per color) [Default 0.0]
-bpp <Bases Per Pixel>[Default : 500 for BNX OR CMAP files]. Example : -bpp 510 will rescale all -i input BNX or CMAP map sizes by 510/500

-res <resolution in pixels>[Default 3.5] : Depends on bpp value
-resSD <standard deviation of resolution in pixels>[Default 0.75] : Depends on bpp value
-reskb <resolution in kb>[Default 1.75]
-reskbSD <standard deviation of resolution in kb [Default 0]
-mres <pixels> : Reduces resolution of -i input maps to specified number of pixels [Default: 0.001] : depends in bpp value
-mresSD <pixelsSD> : Varies the resolution of -i input maps by randomly varying -mres value by specified Gaussian SD. [Default 0]: introduces randomness in map resolution


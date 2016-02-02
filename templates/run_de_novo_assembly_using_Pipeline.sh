#!/bin/bash
#SBATCH --time=72:00:00
#SBATCH --mem=1024M

if [[ "$1" == "" ]]
then
  echo "USAGE: ./run_de_novo_assembly_using_Pipeline.sh <input.bnx>"
  exit 1
fi

# 1. Find all necessary files
export SGE_ROOT=/Their/software/does/not/even/use/this/value
export DRMAA_LIBRARY_PATH=/fslgroup/fslg_bionano/lib/lib/libdrmaa.so ### SET ME
PYTHON=/fslhome/jtpage/bin/python ###SET ME
SCRIPTS_DIR=/fslgroup/fslg_bionano/compute/refined_assemblies/scripts/ ### SET ME
TOOLS_DIR=/fslgroup/fslg_bionano/compute/refined_assemblies/tools/ ### SET ME

INPUT_FILE="$1"
OUTPUT_DIR=./`echo "$INPUT_FILE" | sed 's/.*\///' | sed 's/\.bnx//'` ### SET ME MAYBE
OPTARGS_FILE="$OUTPUT_DIR/optArguments.xml" ### SET ME MAYBE
CLUSTERARGS_FILE=$SCRIPTS_DIR/clusterArguments.xml ### SET ME MAYBE
LOG_FILE="$OUTPUT_DIR/$OUTPUT_DIR.log" ### SET ME MAYBE

# 2. Test that all necessary files are found
ERROR_MESSAGE=""
if [ ! -e "$DRMAA_LIBRARY_PATH" ]; then
  ERROR_MESSAGE="$ERROR_MESSAGE""Unable to find DRMAA library path: $DRMAA_LIBRARY_PATH
"; fi
if [ ! -x $PYTHON ]; then
  ERROR_MESSAGE="$ERROR_MESSAGE""$PYTHON is not executable
"; fi
if [ ! -e "$SCRIPTS_DIR"/pipelineCL.py ]; then
  ERROR_MESSAGE="$ERROR_MESSAGE""$SCRIPTS_DIR is incorrectly formatted (it is missing pipelineCL.py
"; fi
if [ ! -e "$TOOLS_DIR"/RefAligner ] || [ ! -e "$TOOLS_DIR"/Assembler ]; then
  ERROR_MESSAGE="$ERROR_MESSAGE""$TOOLS_DIR is incorrectly formatted
"; fi
if [ ! -e "$CLUSTERARGS_FILE" ]; then
  ERROR_MESSAGE="$ERROR_MESSAGE""Cluster args file $CLUSTERARGS_FILE does not exist
"; fi
if [ ! -e "$INPUT_FILE" ]; then
  ERROR_MESSAGE="$ERROR_MESSAGE""Input file $INPUT_FILE does not exist
"; fi
if [ ! -d "$OUTPUT_DIR" ]; then
  ERROR_MESSAGE="$ERROR_MESSAGE""Output directory $OUTPUT_DIR does not exist
"; fi
if [ ! -e "$OPTARGS_FILE" ]; then
  ERROR_MESSAGE="$ERROR_MESSAGE""optArgs file $OPTARGS_FILE does not exist
"; fi
if [[ "$ERROR_MESSAGE" != "" ]]; then
  echo "$ERROR_MESSAGE"
  exit 1
fi

# 3. Run assembly
echo ------------- NEW RUN ------------- >> $LOG_FILE
date >> $LOG_FILE
printenv >> $LOG_FILE

$PYTHON $SCRIPTS_DIR/pipelineCL.py -U -d -T 12 -j 8 -N 2 -i 5 -a "$OPTARGS_FILE" -w -t "$TOOLS_DIR" -l "$OUTPUT_DIR/output" -b "$INPUT_FILE" -C "$CLUSTERARGS_FILE" 2>&1 >> $LOG_FILE 

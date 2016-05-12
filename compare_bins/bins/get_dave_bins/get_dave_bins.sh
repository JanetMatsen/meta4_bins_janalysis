#!/usr/bin/env bash

# change current directory to that of script
cd "$(dirname "$0")"

# bins are stored at :
# e.g. head /work/dacb/elvizAnalysis/checkM_individual/results/elviz-contigs-1056274.Methylomonas-1/elviz-contigs-1056274.Methylomonas-1.fna

# the favorite bins (540 of them) were e-mailed to Janet on 5/10
# Janet saved them locally, moved a copy in .tsv format via sshfs, and is grabbing them from /work/dacb/elvizAnalysis/.

BIN_NAMES=`awk 'NR>1 {print $1}' 160510_interesting_bins_dave_made.tsv` 
#echo $BIN_NAMES
PATH_TO_BINS="/work/dacb/elvizAnalysis/results/"

# keep track of bins we couldn't find (shouldn't be any)
MISSING_BINS=""

# Grab them one by one
for BIN in $BIN_NAMES
do 
  BIN_PATH="${PATH_TO_BINS}${BIN}.fna"
  #echo $BIN_PATH""
  #ls -l $BIN_PATH
  cp $BIN_PATH ../fasta_files
  # if the exit status wasn't zero, store 
  if [ $? -ne 0 ]
  then
      MISSING_BINS=${MISSING_BINS} ${BIN}
  fi
done

echo "missing bins:"
echo $MISSING_BINS


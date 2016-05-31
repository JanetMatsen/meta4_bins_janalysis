#!/usr/bin/env bash

# change current directory to that of script
cd "$(dirname "$0")"

# prepare a folder to keep them in
DEST_DIR='./bins/'
echo "make directory to store copies of bins: $DEST_DIR"
mkdir -p $DEST_DIR

# just copy the fauzi bins.
# Eventually fix so they are cleanly generated here?
cp /gscratch/lidstrom/meta4_bins/janalysis/compare_fauzi_bins/individual_bins/* $DEST_DIR

# change all the file names from .fasta to .fna to be consistent with Dave. 
for file in $DEST_DIR/*.fasta ; do mv $file `echo $file | sed 's/\(.*\.\)fasta/\1fna/'` ; done

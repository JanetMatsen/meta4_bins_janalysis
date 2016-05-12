#!/usr/bin/env bash

# change current directory to that of script
cd "$(dirname "$0")"

# prepare a folder to keep the bins in
DEST_DIR=./bins
echo "make directory to store copies of bins: $DEST_DIR"
mkdir -p $DEST_DIR


# Loop over the bins that we want and make a copy of each in this dir. 
while read line; do
  file_name=$line
  file_path="/work/dacb/extract_isolates/${file_name}"
  ls -l $file_path
	#"/work/dacb/extract_isolates/${file_name}"
cp $file_path $DEST_DIR
done < isolate_bins_to_get

# change all bin names from .fasta to .fna, which Dave seems to prefer
for file in $DEST_DIR/*.fasta ; do mv $file `echo $file | sed 's/\(.*\.\)fasta/\1fna/'` ; done

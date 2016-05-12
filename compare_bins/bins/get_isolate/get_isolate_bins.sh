#!/usr/bin/env bash

# change current directory to that of script
cd "$(dirname "$0")"

DESTINATION=../fasta_files/

# Loop over the bins that we want and make a copy of each in this dir. 
while read line; do
  file_name=$line
  file_path="/work/dacb/extract_isolates/${file_name}"
  ls -l $file_path
	#"/work/dacb/extract_isolates/${file_name}"
  cp $file_path $DESTINATION
done < isolate_bins_to_get

#!/usr/bin/env bash

# change current directory to that of script
cd "$(dirname "$0")"

# just copy the fauzi bins.
# Eventually fix so they are cleanly generated here?
cp /gscratch/lidstrom/meta4_bins/janalysis/compare_fauzi_bins/individual_bins/* ../fasta_files

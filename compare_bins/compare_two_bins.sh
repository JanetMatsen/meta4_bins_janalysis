#!/bin/bash

echo "use mummer's nucmer to compare $1 to $2"
filename_base="$1_to_$2"
echo "filename: $filename_base"

# run nucmer 
/gscratch/lidstrom/software/MUMmer3.23/nucmer --prefix=mummer_results/$filename_base ./individual_bins/$1.fasta ./individual_bins/$2.fasta
# makes a .delta file that looks like: 
# 0081642_122 Ga0081650_101 52572 22207
# 1 110 1 110 1 1 0
# 0
# >Ga0081642_129 Ga0081650_101 17343 22207
# 2 110 1 110 1 1 0
# -28
# 0

# turn the .delta file into a .coords file:
/gscratch/lidstrom/software/MUMmer3.23/show-coords -rcl ./mummer_results/$filename_base.delta > ./mummer_results/$filename_base.coords

# for now, don't delete the .delta file


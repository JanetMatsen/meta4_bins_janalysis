# steps:

# WARNING:
# 160512: putting all analysis on hold in this dir to work on more general compare_bins dir
Added the following to .gitignore in this dir:
- Develop_mummer_aggregation.ipynb
- checkm/
- dev_bin_tools.ipynb
- percent_identities.tsv

- split_fasta_into_individual_bins makes individual bins
	- calls ag to pull out the names from Fauzi's bins at data/genome_bins.fasta
		- saves results as DNA_names.txt (in support_files dir)
	- runs summarise_bins.py (in support_files dir) to convert those names to file names
		- also writes bin_summary.csv (to support_files dir)
- mummer_all_bins runs mummer on all bins (using envoy) 
	- runs compare_two_bins.sh
- coords_to_csv takes a mummer3 .coords file and parses it to the relevant .tsv

# 
DNA_names.txt --> bin_summary.csv --> individual bins --> bp counted after split.


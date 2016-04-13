# steps:

- split_fasta_into_individual_bins makes individual bins
	- calls ag to pull out the names from Fauzi's bins at data/genome_bins.fasta
		- saves results as DNA_names.txt (in support_files dir)
	- runs summarise_bins.py (in support_files dir) to convert those names to file names
		- also writes bin_summary.csv (to support_files dir)
- mummer_all_bins runs mummer on all bins (using envoy) 
	- runs compare_two_bins.sh
- coords_to_csv takes a mummer3 .coords file and parses it to the relevant .tsv


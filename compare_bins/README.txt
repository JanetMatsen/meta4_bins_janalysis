# steps:

1: extract_names.sh searches for all contig names in /data/genome_bins.fasta
	- saves reults to /compare_bins/DNA_names.txt
2: split genome_bins.fasta into individual bins via split_fasta_into_individual_bins.py
	- populates bins to .fasta files in ./individual_bins
3: contig_distributions.py (run by genome_bin_contig_distributions.ipynb): 
	- reads in DNA_names.txt and parses them
	- uses contig_distributions.py for functions.  # <-- needs to be renamed
	- writes bin_summary.csv, which contains bin names and number of contigs per bin
4: mummer_all_bins runs mummer on all bins (using envoy) 
	- runs compare_two_bins.sh
5: coords_to_csv takes a mummer3 .coords file and parses it to the relevant .tsv


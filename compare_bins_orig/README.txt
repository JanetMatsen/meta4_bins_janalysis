Goal:
- compare metagenome ANI across genome bins from Fauzi, bins from Dave, and isolate genomes. 

Approach:
- Genomes/Bins to compare:
    - individual genome bins from Frauzi broken apart by Janet's python script
    - individual genome bins from Dave
	- he made waaaay too many, but we selected the best ~450 of them
    - isolate genomes.
	only use the list Mila provided, not all 56-ish of them. 
	- broken apart by SQL. See: /work/dacb/extract_isolates
- Analysis method:
  - Use mummer to compare all pairs of bins
      - did a pilot test in 3/2016 using only Fauzi genomes
      - also did checkm for other reasons (fix their names)
  - Aggregate mummer results across a pair to get avg. nucleic acid identity (ANI)
      - just do an average weighting of % identity across contigs.  use best match.    

Strategy:
- copied .fasta files (with .fna ending) into child directories that denote their source
- use python3 to enumerate all the files available
	- calculate # of contigs in each, and # of bp. 
	- save survey to a .tsv file
- use python3 to run mummer against all pairs of files
	- note: substantially re-writing my mummer_all_bins.py file from the preliminary Fazui tests
	- save results to ./mummer_results/
	- check that the resulting file doesn't already exist in ./mummer_results/
	- when all the mummering is done, parse the files
		- uses a python parser leveraged from the internet but improved in the fauzi prelim test dir
	- then calculate ANI from those
		- I only had dipped my toe in when working on Fauzi's files but put it on hold until now.
- make heatmaps of the results
	- don't try to plot everything or it would be a 500 by 500 matrix. 


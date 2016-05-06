Goal:
- compare metagenome ANI across genome bins from Fauzi, bins from Dave, and isolate genomes. 

Approach:
- Genomes/Bins to compare:
    - individual genome bins from Frauzi broken apart by Janet's python script
    - individual genome bins from Dave, broken apart by SQL 
	see: /work/dacb/extract_isolates
    - isolate genomes.
	only use the list Mila provided, not all 56-ish of them. 
- Analysis method:
  - Use mummer to compare all pairs of bins
      - did a pilot test in 3/2016 using only Fauzi genomes
      - also did checkm for other reasons (fix their names)
  - Aggregate mummer results across a pair to get avg. nucleic acid identity (ANI)
      - just do an average weighting of % identity across contigs.  use best match.    



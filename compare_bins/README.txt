Goal:
- compare metagenome average nucleotide identity (ANI) across genome bins 
  from Fauzi, bins from Dave, and isolate genomes.
- This statistic, combined with Mummer completedness and contamination are
  our top tools for identifying favorite genome bins to include in 
  metagenomic analysis and partial correlation analysis. 

Approach:
- Genomes/Bins to compare:
    - all bins in /work/meta4_bins/data/bins.  Includes:
        - isolate genomes (ones Mila selected)
            - originally isolates were downloaded in bulk as a concatenated .fasta file
            - Dave broke apart the .fasta using the script /work/dacb/extract_isolates
            - intended to only use a subset of the bins for ANI analysis, but turns out I used them all 
                - see /work/meta4_bins/data/bins/isolate/get_isolate_genomes.sh
            - file names are made from their descriptions in the genbank and fasta files
            - also makes .gff files via /work/meta4_bins/data/bins/isolate/scripts/make_gff_from_fna.sh
        - Fauzi Bins 
            - uses some renamed bins, as detailed in /work/meta4_bins/data/bins/fauzi/raw
            - moved into /work/meta4_bins/data/bins/fauzi/bins by the script assemble_bins.sh
        - Dave bins:
            - Dave's method made waaaay too many, but we selected the best 497 of them
            - copies over interesting bins from those in a list 
                - original list had some errors, so we use 60510_interesting_bins_dave_made.tsv, not 
                  160510_interesting_bins_dave_made.tsv.original
                - original bins at: /workd/dacb/elvizAnalysis/results/
                - copies over gff from there too. 
            - bins dir has some scripts:
                - gff_fixer (fixes GFF format).  A Dave script. 
- Analysis method:
  - Use mummer to compare all pairs of bins
      - did a pilot test in 3/2016 using only Fauzi genomes
      - scaled to this directory with all bins being used. 
            - the scripts run MUMmer on the bins in  /work/meta4_bins/data/bins

  - Aggregate mummer results across a pair to get avg. nucleic acid identity (ANI)
    - originally just did an average weighting of % identity across contigs. 
        - used best match. 
    - some unrelated bins got high ANI scores, leading us to include a term 
      summarisiing the fraction of the reference genome covered by the alignment. 
    - a 2nd metric was also introduced where you don't just use the longest alignment, but
      allow for all matches to be used.  This can lead to > 100% coverage and > 100% ANI. 

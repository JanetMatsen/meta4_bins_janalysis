Goal:
- compare metagenome ANI across genome bins from Fauzi, bins from Dave, and isolate genomes.

Approach:
- Genomes/Bins to compare:
    - all bins in /work/meta4_bins/data/bins.  Includes:
        - isolate genomes (ones Mila selected)
            - only use the list Mila provided, not all 56-ish of them.
            - copied over from ./originals (which were obtained from Hyak)
            - file names are made from their descriptions in the genbank and fasta files
            - also makes .gff files via /work/meta4_bins/data/bins/isolate/scripts/make_gff_from_fna.sh
        - Fauzi Bins (uses assemble_bins from /work/meta4_bins/data/bins/fauzi/bins
            - J would have put this in /work/meta4_bins/data/bins/fauzi (keep the bins dir clean)
        - Dave bins:
            - Dave's method made waaaay too many, but we selected the best ~450 of them
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
      - started to scale it to the new format: see compare_bis_orig
        - this folder still kept a copy of each of the bins.   
            - the updated version will reference /word/meta4_bins/data/bins

  - Aggregate mummer results across a pair to get avg. nucleic acid identity (ANI)
      - just do an average weighting of % identity across contigs.  use best match. 
    - to do: keep track of the fraction of the length that is accounted for. 

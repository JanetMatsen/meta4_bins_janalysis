#! /usr/bin/env python
# Note: you need to `source activate py2` before running this script. 
# So far, I have only shown envoy to run with python 2.

# Note: you can't point to a virtualenv python in the shebang.  Boo!  
# You need to `source_activate meta4` before calling the .py file. 
# #! /home/jmatsen/miniconda2/envs/meta4/bin python

import os

import unused_reads as ur

#print the python path being used. 
try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
except KeyError:
    user_paths = []

# run the command

# word size = 11 is default for blastn
# see: http://www.ncbi.nlm.nih.gov/books/NBK279675/
# Note it is for the initial match:
# "Number of matching nucleotides in initial match."

# do the unmapped
ur.downsample_fasta_and_blast(parent_directory='./unmapped-final',
                              samples_to_investigate=ur.SAMPLES,
                              downsample_granularity=1000,
                              blast_db='nt',
                              word_size=24, max_target_seqs=1, threads=3)

# do the multiply mapped
ur.downsample_fasta_and_blast(parent_directory='./multiply_mapped-final',
                              samples_to_investigate=ur.SAMPLES,
                              downsample_granularity=1,
                              blast_db='bins',
                              word_size=24, max_target_seqs=1, threads=3)








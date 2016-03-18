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

ur.run_pipeline(samples_to_investigate=ur.SAMPLES,
                parent_directory='./unmapped-final',
                blast_db='nt',
                verbose=True, sam_flag='unmapped',
                downsample_fasta=10000, word_size=24,
                max_target_seqs=1)

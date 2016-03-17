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

# file to write messages/tests(?) to:
STD_OUT = 'run_history.out'
# path to the workspace dirs like LakWasM112_LOW13_2/


ur.shell("uptime", STD_OUT)
ur.shell("pwd", STD_OUT)

# make sure the dirs I want exist.
dirs = ['fasta_files', 'blast_results']
for d in dirs:
    ur.create_dir(d)


# /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam
# /gscratch/lidstrom/meta4_bins/workspace/LakWasMet70_HOW9_2/bwa/LakWasMet70_HOW9_2.sorted.bam
# /gscratch/lidstrom/meta4_bins/workspace/LakWasMe82_HOW10_2/bwa/LakWasMe82_HOW10_2.sorted.bam
samples_to_investigate = ['112_LOW13']

FASTA_FOLDER = 'fasta_files'
BLASTED_FOLDER = 'blasted'

ur.create_dir(FASTA_FOLDER)
ur.create_dir(BLASTED_FOLDER)

def run_pipeline(verbose=True, downsample_fasta=1000):
    for sample in samples_to_investigate:
        if verbose:
            print("start work for sample: {}".format(sample))

        # get the path to the original BAM file
        bam_file = ur.sample_name_to_bam_filepath(sample)
        if verbose:
            print("bam file path: {}".format(bam_file))

        # identify a filepath/name for the output fasta
        sample_fasta = ur.sample_name_to_fasta_name(sample)

        if ur.check_file_exists(sample_fasta):
            print("fasta {} exists already; don't make from .bam".format(
                sample_fasta))
        else:
            print("generate .fasta for {}".format(sample))
            ur.bam_to_fasta(source_bam=bam_file,
                            dest_fasta=sample_fasta,
                            sam_flag=4)
        # check that the blasted file exists now.
        assert(ur.check_file_exists(sample_fasta))

        # downsample the fasta so BLAST doesn't take *forever*
        # downsample_fasta() returns path to downsampled fasta.
        downsampled_fasta = ur.downsample_fasta(sample_fasta, downsample_fasta)


        # blast the results
        sample_blasted = \
            ur.sample_name_to_blasted_name(sample +
                                           "_" + str(downsample_fasta))
        print('blast downsampled fasta.  Store results as {}'.format(
            sample_blasted))
        # do the blasting
        # remove old file if its length is zero
        if ur.check_file_exists(sample_blasted):
            with open(sample_blasted) as f:
                num_lines = len(f.readlines())
            if num_lines != 0:
                print("fasta {} already exists.".format(sample_blasted))
        else:
            print("blast {} and save as {}".format(downsampled_fasta,
                                                   sample_blasted))
            ur.blast_fasta(in_file=downsampled_fasta,
                           out_file=sample_blasted)
        # check that the blasted file exists now.
        assert(ur.check_file_exists(sample_blasted))

run_pipeline()









        # get the reads





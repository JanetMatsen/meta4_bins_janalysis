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


def run_pipeline(samples_to_investigate, parent_directory,
                 verbose=True, sam_flag='unmapped',
                 downsample_fasta=10000, word_size=24,
                 max_target_seqs=1):

    # todo: sanatize so parent_directory could be './dirname' or './dirname'
    # or 'dirname' etc.
    ur.create_dir(parent_directory)
    ur.create_dir(parent_directory + '/fasta_files')
    ur.create_dir(parent_directory + '/blast_results')

    for sample in samples_to_investigate:
        if verbose:
            print("start work for sample: {}".format(sample))

        # get the path to the original BAM file
        bam_file = ur.sample_name_to_bam_filepath(sample)
        if verbose:
            print("bam file path: {}".format(bam_file))

        # identify a filepath/name for the output fasta
        sample_fasta = ur.sample_name_to_fasta_path(sample, parent_directory)

        if ur.check_file_exists(sample_fasta):
            print("fasta {} exists already; don't make from .bam".format(
                sample_fasta))
        else:
            print("generate .fasta for {}".format(sample))
            ur.bam_to_fasta(source_bam=bam_file,
                            dest_fasta=sample_fasta,
                            sam_flag=sam_flag)
        # check that the blasted file exists now.
        assert(ur.check_file_exists(sample_fasta))

        # downsample the fasta so BLAST doesn't take *forever*
        # downsample_fasta() returns path to downsampled fasta.
        downsampled_fasta = ur.downsample_fasta(sample_fasta, downsample_fasta)

        # blast the results
        sample_blasted = \
            ur.sample_name_to_blasted_path(
                sample + "_" + str(downsample_fasta),
                parent_directory)
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
                           out_file=sample_blasted,
                           word_size=word_size,
                           max_target_seqs=max_target_seqs)
        # check that the blasted file exists now.
        assert(ur.check_file_exists(sample_blasted))

# run the command
run_pipeline(samples_to_investigate=ur.SAMPLES,
             parent_directory='./unmapped',
             verbose=True, sam_flag='unmapped',
             downsample_fasta=10000, word_size=24,
             max_target_seqs=1)

run_pipeline(samples_to_investigate=ur.SAMPLES,
             parent_directory='./multiply_mapped',
             verbose=True, sam_flag='multiple',
             downsample_fasta=10000, word_size=24,
             max_target_seqs=3)











        # get the reads





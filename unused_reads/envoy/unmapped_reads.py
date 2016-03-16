#! /usr/bin/env python
# Note: you need to `source activate meta4` before running this script. 

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

std_out = 'run_history.out'

ur.shell("uptime", std_out)
ur.shell("pwd", std_out)

# make sure the dirs I want exist.
dirs = ['fasta_files', 'blast_results']
for d in dirs:
    ur.create_dir(d)


# /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam
# /gscratch/lidstrom/meta4_bins/workspace/LakWasMet70_HOW9_2/bwa/LakWasMet70_HOW9_2.sorted.bam
# /gscratch/lidstrom/meta4_bins/workspace/LakWasMe82_HOW10_2/bwa/LakWasMe82_HOW10_2.sorted.bam
samples_to_investigate = ['112_LOW13']

# todo: use function to get .bam file paths.
bam_files = \
    ['/gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam']


def run_pipeline(verbose=True):
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
            ur.bam_to_fasta(source_path = bam_file,
                            dest_path=sample_fasta,
                            std_out_file=std_out,
                            sam_flag=4, header=True, subsample=0.01)

       # demo of blasting the results:
        ur.blast_fasta(in_file='./dev/50.fasta',
                       out_file='./dev/50_blasted.tsv')

        # # blast the results
        # sample_blasted = ur.sample_name_to_blasted_name(sample)
        # if not ur.check_file_exists(sample_blasted):
        #     ur.blast_fasta(in_file = sample_fasta,
        #                    out_file = sample_blasted,
        #                    outfmt=None)
        # # check that it exists now.
        # assert(ur.check_file_exists(sample_blasted))

run_pipeline()









        # get the reads





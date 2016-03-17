#! /usr/bin/env python

import os

import unused_reads as ur

# this worked:
# ur.shell('echo "this is write_long_file.py"')
# ur.shell("cat more_than_55.fasta", 'long_cat_from_envoy.fasta')

print("""
    this
    is
    multiline
    """)

SAMPLE = '112'
RUN_NAME = 'no_sam'
RUN_BLAST=False

FILE_DIR = './dev-'+RUN_NAME + '/'
print("directory to save files in: {}".format(FILE_DIR))
ORIGINAL_BAM = ur.sample_name_to_bam_filepath(SAMPLE)
DOWNSAMPLED_BAM = FILE_DIR + SAMPLE + '.bam'
DOWNSAMPLED_FASTA = FILE_DIR + SAMPLE + '.fasta'
DOWNSAMPLED_TSV = FILE_DIR + SAMPLE + '.tsv'

# make the directory
ur.create_dir(FILE_DIR)


def subsample_bam_to_bam(in_bam, out_bam, downsample_frac):
    # subsample a bam file and save it at the place out_bam.
    # used for developing a faster test of my methods.
    if ur.check_file_exists(out_bam):
        pass
    #command = '/work/software/samtools/bin/samtools view -f 256 -h  '
    command = """/work/software/samtools/bin/samtools \
                 view -s {} -h {}""".format(downsample_frac, in_bam)
    print("command to make downasmpled bam: \n   {}".format(command))
    # - > ./fasta_files/57_HOW8_2--subsampled.fasta"
    ur.shell(command, outfile=out_bam, debug=False)


def make_test_bam(downsample_frac=0.02):
    # grab a .bam file, use samtools to get a downsampled fraction.
    in_bam = ORIGINAL_BAM
    # prepare a file name to save the result as
    out_bam = DOWNSAMPLED_BAM
    if not ur.check_file_exists(out_bam):
        subsample_bam_to_bam(
            # can wrap line across rows.
            # Don't use triple quotes or the new lines will be stored.
            in_bam=in_bam,
            out_bam=out_bam,
            downsample_frac=downsample_frac)
    # todo: report the fraction of the file size.
    pass

# The downsampled file is 0.6% as big as the original.  (frac = 0.006)
# $ ls -lshR  ./dev/downsampled_112.bam
# 18M -rw-r--r-- 1 jmatsen users 18M Mar 17 06:59 ./dev/downsampled_112.bam

# $ ls -lshR  /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam
# 3.0G -rwxrwx--- 1 dacb users 3.0G Feb  5 19:49 \
    # for  /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam

print("starting directory:")
ur.shell("ls -lshR " + FILE_DIR)

make_test_bam()


def test_bam_to_fasta():
    # remove the old fasta if it exists:
    in_bam = DOWNSAMPLED_BAM
    out_fasta = DOWNSAMPLED_FASTA
    if ur.check_file_exists(out_fasta):
        print("file {} exists.  Delete and re-make it.".format(out_fasta))
        os.remove(out_fasta)
    # Make the .fasta file
    print("Make {}".format(out_fasta))
    ur.bam_to_fasta(source_bam=in_bam, dest_fasta=out_fasta,
                    debug=True, intermediate_sam=False)
    # Print the directory contents
    print('ls -lshR {}'.format(FILE_DIR))
    ur.shell('ls -lshR {}'.format(FILE_DIR))


test_bam_to_fasta()


def test_blast_fasta():
    # blast the .fasta file made by test_bam_to_fasta()
    in_fasta = DOWNSAMPLED_FASTA
    out_tsv = DOWNSAMPLED_FASTA
    ur.blast_fasta(in_fasta, out_tsv, outfmt=None)
    pass

# BLAST takes a long time to run.  Only run it if it was specified at the top.
if RUN_BLAST:
    test_blast_fasta()


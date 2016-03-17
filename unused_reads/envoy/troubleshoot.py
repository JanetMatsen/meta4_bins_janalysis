#! /usr/bin/env python

import unused_reads as ur

# this worked:
# ur.shell('echo "this is write_long_file.py"')
# ur.shell("cat more_than_55.fasta", 'long_cat_from_envoy.fasta')

print("""
    this
    is
    multiline
    """)

def subsample_bam_to_bam(in_bam, out_bam):
    # subsample a bam file and save it at the place out_bam.
    # used for developing a faster test of my methods.
    if ur.check_file_exists(out_bam):
        pass
    #command = '/work/software/samtools/bin/samtools view -f 256 -h  '
    command = """/work/software/samtools/bin/samtools \
                 view -s 0.001 {}""".format(in_bam)
    print("command to run: {}".format(command))
    # - > ./fasta_files/57_HOW8_2--subsampled.fasta"
    ur.shell(command, outfile=out_bam, debug=False)


def make_test_bam():
    # grab a .bam file, use samtools to get just 10% of it.
    subsample_bam_to_bam(
        in_bam="/gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2"
               "/bwa/LakWasM112_LOW13_2.sorted.bam",
        out_bam='./dev/tenth_112.bam')
    pass
# ls -l /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam

# (py2)jmatsen@waffle:/gscratch/lidstrom/meta4_bins/janalysis/unused_reads
## /envoy$ ls -l ./dev/tenth_112.bam #
#-rw-r--r-- 1 jmatsen users 204,244,448 Mar 16 21:29 ./dev/tenth_112.bam #
#(py2)jmatsen@waffle:/gscratch/lidstrom/meta4_bins/janalysis/unused_reads # /envoy$ ls -l /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam
# -rwxrwx--- 1 dacb users 3,162,655,566 Feb  5 19:49
# /gscratch/lidstrom/meta4_bins/workspace/LakWasM112_LOW13_2/bwa/LakWasM112_LOW13_2.sorted.bam

make_test_bam()



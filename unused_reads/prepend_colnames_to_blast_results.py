#!/usr/bin/python

import os

blast_header = "stitle	qseqid	sseqid	pident	length	evalue	bitscore	mismatch	gapopen	qstart	qend	sstart	send"


def prepend_header(filename):
    with open(filename, 'r') as original:
        data = original.read()
        print(data[0:20])
        if data[0:20] == blast_header[0:20]:
            print("don't add header")
        else:
            print("add header")
            with open(filename, 'w') as modified:
                modified.write(blast_header + "\n" + data)


# todo: use glob instead
def walk_dir(dir):
    for i in os.listdir(dir):
        print i
        if i.endswith("blasted.tsv"):
            print("dir: {}".format(i))
            prepend_header(dir + i)


# test it on a file:
# prepend_header("/work/meta4_bins/janalysis/unused_reads/unmapped/blast_results/tmp-blasted.tsv")

# test file:
# dirs_to_fix = ['./unmapped-final_toy/blast_results/']

dirs_to_fix = [
    '/gscratch/lidstrom/meta4_bins/janalysis/unused_reads/'
    'unmapped-final/blast_results/',
    '/gscratch/lidstrom/meta4_bins/janalysis/unused_reads/'
    'multiply_mapped-final/blast_results/'
    ]

for dirname in dirs_to_fix:
    print(dirname)
    print(os.listdir(dirname))
    walk_dir(dirname)

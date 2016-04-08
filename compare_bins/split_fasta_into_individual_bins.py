import os
import re
import sys
print(sys.path)
import pandas as pd
# from optparse import OptionParser
from Bio import SeqIO

def lookup_filename(record):
    bin = re.search('(Ga[0-9]+)_', record.id).group(1)
    filename_array = bin_df[bin_df['bin'] == bin]['file name'].values
    # There is a problem if more than one file name matched.
    assert len(filename_array) == 1, \
        'need only 1 selected; had {}'.format(filename_array)
    # return the file name for the match.
    filename = filename_array[0]
    # replace spaces with _
    filename = filename.replace(" ", "_")
    return filename


bin_df = pd.read_csv('./bin_summary.csv')

usage = "usage: %prog fasta_file_in directory_out"
# parser = OptionParser(usage)
# (opts, args) = parser.parse_args()
dir_out = os.getcwd() + '/individual_bins'

file_in = '/gscratch/lidstrom/meta4_bins/data/genome_bins.fasta'
dir_out = './individual_bins'


for record in SeqIO.parse(open(file_in), "fasta"):
    f_name = lookup_filename(record)
    f_out = os.path.join(dir_out, f_name + '.fasta')
    print('filename: {}'.format(f_out))
    SeqIO.write([record],open(f_out,'a'),"fasta")

print(bin_df.head())



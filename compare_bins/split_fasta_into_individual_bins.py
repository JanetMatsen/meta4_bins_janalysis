import re
import sys
print(sys.path)
import pandas as pd

from Bio import SeqIO
import os

import summarise_bins

# first extract the bin names
# replaces extract_names.sh, which searched for all contig names in
# /data/genome_bins.fasta and saved reults to /compare_bins/DNA_names.txt

# use os, not envoy this time.  I haven't shown envoy to be good w/ Python3
os.system("""ag --max-count 9999999 ">" /gscratch/lidstrom/meta4_bins/data/genome_bins.fasta > /gscratch/lidstrom/meta4_bins/janalysis/compare_bins/DNA_names.txt""")

# call summarise_bins to make bin_summary.csv
#summarise_bins.main()
# exec(open("./filename").read())
exec(open("summarise_bins.py").read())
# exec(open("./path/to/script.py").read(), globals())
# This will execute a script and put all it's global variables in the
# interpreter's global scope (the normal behavior in most other languages).

# make dir individual_bins
if not os.path.exists('./individual_bins'):
    os.makedirs('./individual_bins')


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
    SeqIO.write([record], open(f_out,'a'), "fasta")

print(bin_df.head())



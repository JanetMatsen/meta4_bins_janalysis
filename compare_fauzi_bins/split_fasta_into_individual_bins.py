import re
import sys
print(sys.path)
import pandas as pd

from Bio import SeqIO
import os


def lookup_filename(record):
    bin = re.search('(Ga[0-9]+)_', record.id).group(1)
    filename_array = bin_df[bin_df['bin'] == bin]['bin name'].values
    # There is a problem if more than one file name matched.
    assert len(filename_array) == 1, \
        'need only 1 selected; had {}'.format(filename_array)
    # return the file name for the match.
    filename = filename_array[0]
    # replace spaces with _
    filename = filename.replace(" ", "_")
    return filename


def make_filename(bin_name):
    return os.path.join(dir_out, bin_name, '.fasta')


def erase_existing_file(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)
    else:
        print("file {} doesn't exist".format(file_name))
    return


def recreate_bins():
    # keep track of bins we have erased and started fresh
    initialized_bins = []
    for record in SeqIO.parse(open(file_in), "fasta"):
        f_name = lookup_filename(record)
        f_out = os.path.join(dir_out, f_name + '.fasta')
        # if it isn't in initialized_bins, it doesn't exist or needs to be
        # wiped.
        if f_out not in initialized_bins:
            # erase file so we don't cat onto an old one.
            erase_existing_file(f_out)
            initialized_bins.append(f_out)
        else:
            print('filename: {}'.format(f_out))
            SeqIO.write([record], open(f_out, 'a'), "fasta")



if __name__ == '__main__':
    support_dir = './support_files/'

    if not os.path.exists(support_dir):
        os.makedirs(support_dir)

    # first extract the bin names
    # replaces extract_names.sh, which searched for all contig names in
    # /data/genome_bins.fasta and saved reults to /compare_bins/DNA_names.txt

    # use os, not envoy this time.  I haven't shown envoy to be good w/ Python3
    os.system(
        'ag --max-count 9999999 ">" '
        '/gscratch/lidstrom/meta4_bins/data/genome_bins.fasta > '
        '/gscratch/lidstrom/meta4_bins/janalysis/'  # path continued
        'compare_bins/support_files/DNA_names.txt')

    # call summarise_bins to make bin_summary.csv
    # summarise_bins.main()
    # exec(open("./filename").read())
    exec(open(support_dir + "summarise_bins.py").read())
    # exec(open("./path/to/script.py").read(), globals())
    # This will execute a script and put all it's global variables in the
    # interpreter's global scope (the normal behavior in most other languages).

    # make dir individual_bins
    if not os.path.exists('./individual_bins'):
        os.makedirs('./individual_bins')

    bin_df = pd.read_csv(support_dir + '/bin_summary.csv')

    usage = "usage: %prog fasta_file_in directory_out"
    # parser = OptionParser(usage)
    # (opts, args) = parser.parse_args()
    dir_out = os.getcwd() + '/individual_bins'

    file_in = '/gscratch/lidstrom/meta4_bins/data/genome_bins.fasta'
    dir_out = './individual_bins'

    recreate_bins()

    # call bin_lengths.py
    # Also reports tim
    exec(open(support_dir + "bin_lengths.py").read())

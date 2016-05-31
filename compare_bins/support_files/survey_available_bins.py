import glob
import os
import re

from Bio import SeqIO
import pandas as pd

# GOAL: use python3 to enumerate all the files available
# calculate # of contigs in each, and # of bp.
# save survey to a .tsv file

# Step 1: loop over all the bins in all the 3 directories and
# get info about them.


def bin_contig_count(bin_path):
    # SeqIO.parse returns a generator.  You can make it a list if you
    # do so right off the bat, but you can't store the generator and
    # turn it into a list later, for some reason.
    bin_list = list(SeqIO.parse(bin_path, 'fasta'))
    return len(bin_list)


def bin_length(bin_path):
    bin_generator = SeqIO.parse(bin_path, 'fasta')
    lengths = map(lambda seq: len(seq.seq), bin_generator)
    return sum(lengths)


def find_all_bins(head_dir, bin_suffix, verbose=False):
    bin_paths = []
    bin_dirs = [head_dir + "/bins/*/bins/*" + bin_suffix]
    path_possibilities = head_dir + "/bins/*/bins/*" + bin_suffix
    print("path possibilities: {}".format(path_possibilities))
    bin_paths = glob.glob(path_possibilities)
    print("number of bin paths: {}".format(len(bin_paths)))
    assert len(bin_paths) > 0, "bin paths not found.  Are you in right dir?"
    return bin_paths


def bin_source_from_path(bin_path):
    pattern = re.compile(r"/bins/([a-zA-Z0-9_]+)/*")
    m = pattern.search(bin_path)
    name = m.group(1)
    #print(name)
    rename_dict = {'isolate_genomes': "isolate",
                   'dave_bins': "dave elviz",
                   'fauzi_bins': "fauzi"}
    assert name in rename_dict.keys(), \
        'Name "{}" is not recognized'.format(name)
    return rename_dict[name]


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    pass


# loop over the bins and collect a list of dicts
def bin_info_dicts():
    # make a list with one dict per bin
    bin_info_list = []
    bin_path_list = find_all_bins(head_dir=".", bin_suffix=".fna")
    # list of possible locations:
    # make a list of bin b
    for bin_path in bin_path_list:
        bin_info = {"bin path": bin_path}

        # pick out just the name
        bin_info["name"] = os.path.basename(bin_path).rstrip(".fna")

        # pick out the source of the bin
        bin_info['category'] = bin_source_from_path(bin_path)

        # find and save the bin's number of base pairs
        bin_bp = bin_length(bin_path)  # TODO: fill in bin_length()
        bin_info['bp'] = bin_bp
        # find and save the bin's number of contigs
        bin_contigs = bin_contig_count(bin_path)  # TODO: fill in function
        bin_info['contigs'] = bin_contigs
        bin_info_list.append(bin_info)
    return bin_info_list

# panda-ify the info made by bin_info_dicts()
def bin_info_pandas():
    bin_info_list = bin_info_dicts()
    print("combine info about {} bins into a pandas df".format(
        len(bin_info_list)))
    df = pd.DataFrame(bin_info_list)
    return df


if __name__ == "__main__":
    print("running mummer_all_bins.py via __name__ == __main__")

    df = bin_info_pandas()
    print(df.head())
    df.to_csv('./support_files/available_bins.csv', index=False)
    

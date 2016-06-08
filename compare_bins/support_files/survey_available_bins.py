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


def first_fasta_contig_name_and_id(bin_path):
    bin_generator = SeqIO.parse(bin_path, 'fasta')
    one_contig = next(bin_generator)
    return {'id': one_contig.id, 'name': one_contig.name}



def find_all_bins(bin_dir, bin_suffix, verbose=False):
    #bin_paths = []
    #bin_dirs = [bin_dir + "/bins/*/bins/*" + bin_suffix]
    path_possibilities = bin_dir + "/*/bins/*" + bin_suffix
    print("path possibilities: {}".format(path_possibilities))
    bin_paths = glob.glob(path_possibilities)
    print("number of bin paths: {}".format(len(bin_paths)))
    assert len(bin_paths) > 0, "bin paths not found.  Are you in right dir?"
    return bin_paths


def bin_source_from_path(bin_path):
    pattern = re.compile(r"/bins/([a-zA-Z0-9_-]+)/*")

    m = pattern.search(bin_path)
    assert m is not None, "no regex match for {}".format(bin_path)
    name = m.group(1)

    #print(name)
    rename_dict = {'isolate': "isolate",
                   'dave': "dave",
                   'fauzi': "fauzi"}
    assert name in rename_dict.keys(), \
        'Name "{}" is not recognized'.format(name)

    bin_category = rename_dict[name]
    #print("bin name for {}: {}".format(bin_path, bin_category))
    return bin_category


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    pass


def extract_bin_number(string):
    # Ga0081607_1001 --> Ga0081607
    m = re.search("(Ga[0-9]+)_[0-9]+", string)
    assert m, 'no match found in {}'.format(string)
    return m.group(1)


# loop over the bins and collect a list of dicts
def bin_info_dicts(bin_dir):
    # make a list with one dict per bin
    bin_path_list = find_all_bins(bin_dir=bin_dir, bin_suffix=".fasta")
    # list of possible locations:
    # make a list of bin b
    bin_info_list = []
    for bin_path in bin_path_list:
        bin_info = {"bin path": bin_path}

        # pick out just the name
        bin_info["name"] = os.path.basename(bin_path).rstrip("\.fasta")


        # pick out the source of the bin
        bin_category = bin_source_from_path(bin_path)
        bin_info['category'] = bin_category

        # find and save the bin's number of base pairs
        bin_bp = bin_length(bin_path)
        bin_info['bp'] = bin_bp

        # find and save the bin's number of contigs
        bin_contigs = bin_contig_count(bin_path)
        bin_info['contigs'] = bin_contigs

        # get the name of the first contig:
        contig_id_and_name_dict = first_fasta_contig_name_and_id(bin_path)

        if bin_category == 'isolate':
            # TODO: stuff
            bin_info_list.append(bin_info)
        else:

            # get the general Ga_ type id for each bin
            first_contig_id = contig_id_and_name_dict['id']
            bin_info['id'] = extract_bin_number(first_contig_id)
            bin_info_list.append(bin_info)

    return bin_info_list


# panda-ify the info made by bin_info_dicts()
def bin_info_pandas(bin_dir):
    # Aggregate the dicts of info about each bin
    bin_info_list = bin_info_dicts(bin_dir)
    print("combine info about {} bins into a pandas df".format(
        len(bin_info_list)))
    df = pd.DataFrame(bin_info_list)
    return df


if __name__ == "__main__":
    print("running mummer_all_bins.py via __name__ == __main__")

    df = bin_info_pandas(bin_dir = '/work/meta4_bins/data/bins')
    print(df.head())
    df.to_csv('./support_files/available_bins.csv', index=False)
    

import os
import subprocess

import pandas as pd

# Load the summary:

def load_summary():
    return pd.read_csv('support_files/bin_summary.csv')


def bin_names_to_coords_filepath(query_bin, ref_bin):
    """
    prepare a file path for results
    :param query_bin: bin number 1 name/filepath (reference sequence)
    :param ref_bin: bin number 2 name/filepath.  (query sequence)
    :return:string like Acidovora-69x_Ga0081644_to_Acidovorax-79_Ga0081651
    """
    outpath = results_dir
    return outpath + '/' + query_bin + "_to_" + ref_bin


def mummer_list_of_bins(bins_list):
    """
    run mummer on all pairs of bins.  Saves results to ./mummer_results/

    :return:
    """
    for query_bin in bins_list:
        # prepare to iterate over all the bins
        bins_to_compare_to = bins_list.copy()

        # loop over all the bins, including itself.
        for ref_bin in bins_to_compare_to:

            # prepare a prefix for mummer to use.
            delta_prefix = bin_names_to_coords_filepath(query_bin=query_bin,
                                                        ref_bin=ref_bin)
            print('.delta file prefix: {}'.format(delta_prefix))

            # Make the .delta file
            # for now allow mummer to run against itself; this is a control.
            # run these commands:
            # USAGE: nucmer  [options]  <Reference>  <Query>
                # so reference is first, then query.
            subprocess.check_call(
                ['/work/software/MUMmer3.23/nucmer',
                '--prefix={}'.format(delta_prefix),
                './individual_bins/' + ref_bin + '.fasta',
                './individual_bins/' + query_bin + '.fasta'])
            # -o makes a .coords file without running show-coords,
            # but makes the .coords file without coverage columns.

            coords_path = open(delta_prefix + '.coords', 'w')
            print('coords_path: {}'.format(coords_path))
            subprocess.check_call(
                ['/work/software/MUMmer3.23/show-coords',
                 '-rcl', str(delta_prefix + '.delta')],
                 stdout=coords_path)


def parse_coords():
    """
    write a .tsv file for each .coords file

    :return:None
    """
    coords_files = os.listdir(results_dir)
    # get just the .coords list (get rid of .delta files and anything else)
    coords_files = [c for c in coords_files if '.coords' in c]
    print('coords_files: {}'.format(coords_files))

    # loop over the coords files
    for coords_file in coords_files:
        coords_path = results_dir + '/' + coords_file
        # check that .coords file actually exists
        # todo: won't tell you if you are missing expected .coord files!
        # Note: this if was made to skip over .coords files that don't exist
        #  during development.
        if os.path.exists(coords_path):
            print('analyze {}'.format(coords_file))
            # prepare the filename for the results
            out_file = results_dir + '/' + \
                       coords_file.strip('.coords') + '.tsv'
            # parse .coords into a .tsv
            subprocess.check_call(['python',
                                   str('./support_files/parse_coords.py'),
                                   # input file:
                                   '-i', str(coords_path),
                                   # output file:
                                   '-o', str(out_file)])


if __name__ == '__main__':
    results_dir = './mummer_results'
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

    bins = load_summary()
    print(bins.head())

    # For each bin, use mummer to make a .coords file for each other bin.
    # Do bin A --> bin B, and bin B --> bin A for convenience, even though one
    # result could be enough for both.
    # Do all to all, even though some comparisons are not very meaningful.

    fauzi_bins_list = bins['bin name'].tolist()
    assert type(fauzi_bins_list) == list, \
        'fauzi_bins_list is not a list: {}'.format(fauzi_bins_list)
    # print('bins_list: {}'.format(bins_list))
    # print('type fo bins_list: {}'.format(type(bins_list)))

    # todo: arguments that specify whether to re-mummer or only parse coords.
    mummer_list_of_bins(fauzi_bins_list)
    parse_coords()


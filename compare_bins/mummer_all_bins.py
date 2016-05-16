import os
import subprocess
import sys

import pandas as pd

# Load the summary:


def load_summary():
   return pd.read_csv('./support_files/bins_available.csv')


def bin_names_to_coords_filepath(query_bin, ref_bin, results_dir):
    """
    prepare a file path for results
    :param query_bin: bin number 1 name/filepath (reference sequence)
    :param ref_bin: bin number 2 name/filepath.  (query sequence)
    :return:string like Acidovora-69x_Ga0081644_to_Acidovorax-79_Ga0081651
    """
    return results_dir + '/' + query_bin + "_to_" + ref_bin


def make_delta_prefix(query_bin_path, ref_bin_path, results_dir):
    delta_prefix = \
        bin_names_to_coords_filepath(
            query_bin=os.path.basename(
                query_bin_path).rstrip(".fna"),
            ref_bin=os.path.basename(ref_bin_path).rstrip(".fna"),
            results_dir=results_dir)
    return delta_prefix


def make_coords_path(query_bin_path, ref_bin_path, results_dir):
    delta_prefix = make_delta_prefix(query_bin_path, ref_bin_path, results_dir)
    coords_path = delta_prefix + '.coords'
    return coords_path


def mummer_two_bins(query_bin_path, ref_bin_path, coords_filepath):
    """
    run mummer on all pairs of bins.  Saves results to ./mummer_results/

    "param bins_list": list of paths to individual bins

    :return: delta_prefix, the filename prefix of the .coords and .delta files.
    This is useful when runing parse_coords() next.
    """
    # prepare a prefix for mummer to use.

    delta_prefix = make_delta_prefix(query_bin_path, ref_bin_path, results_dir)

    print('.delta file prefix: {}'.format(delta_prefix))

    # Make the .delta file
    # for now allow mummer to run against itself; this is a control.
    # run these commands:
    # USAGE: nucmer  [options]  <Reference>  <Query>
    # so reference is first, then query.
    nucmer_call = ['/work/software/MUMmer3.23/nucmer',
                   '--prefix={}'.format(delta_prefix),
                   ref_bin_path, query_bin_path]
    print('command to run: ')
    print(' '.join(nucmer_call))
    subprocess.check_call(nucmer_call)
    # -o makes a .coords file without running show-coords,
    # but makes the .coords file without coverage columns.

    coords_path = make_coords_path(query_bin_path, ref_bin_path, results_dir)
    coords_handle = open(coords_path, 'w')
    print('coords_path: {}'.format(coords_path))

    subprocess.check_call(
        ['/work/software/MUMmer3.23/show-coords',
         '-rcl', str(delta_prefix + '.delta')],
        stdout=coords_handle)

    return coords_path


def parse_coords(coords_path, results_dir):
    """
    write a .tsv file summarising a given .coords file

    :return:None
    """
    # check that .coords file actually exists
    # todo: won't tell you if you are missing expected .coord files!
    # Note: this if was made to skip over .coords files that don't exist
    #  during development.
    if os.path.exists(coords_path):
        print('analyze {}'.format(coords_path))
        # prepare the filename for the results

        out_path = coords_path.rstrip('.coords') + '.tsv'
        print("save parsed coords file to {}".format(out_path))
        # parse .coords into a .tsv
        parse_command = ['python',
                         str('./support_files/parse_coords.py'),
                         # input file:
                         '-i', str(coords_path),
                         # output file:
                         '-o', str(out_path)]
        print('command to parse .coords: {}'.format(" ".join(parse_command)))
        subprocess.check_call(parse_command)


def analyze_all_bin_pairs(bin_paths_list, results_dir, preserve_existing=True):
    """
    loop over a list of bin paths and for every combination of the, run
    mummer then parse the cooresponding .coords file

    :return: nothing to terminal/python but saves files
    """
    for query_bin_path in bin_paths_list:
        # prepare to iterate over all the bins
        bins_to_compare_to = bin_paths_list.copy()

        # loop over all the bins, including itself.
        for ref_bin_path in bins_to_compare_to:
            # first check whether file exists:
            expected_coords_path = make_coords_path(query_bin_path,
                                                    ref_bin_path,
                                                    results_dir)
            coords_exists = os.path.exists(expected_coords_path)
            if preserve_existing:
                if not coords_exists:
                    coords_path = mummer_two_bins(query_bin_path,
                                                  ref_bin_path,
                                                  results_dir)
                else:
                    # don't remake the file if it already exists.
                    continue
            # If we don't care whether the file exists or not, make it
            # fresh every time.
            else:
                    coords_path = mummer_two_bins(query_bin_path,
                                                  ref_bin_path,
                                                  results_dir)
            print(coords_path)

            # parse the coords file we just made
            # todo: currently regenerating whether or not coords file was
            # preserved.  But this is fast, so maybe just leave it.
            print("--------- parse file: {} ------------".format(coords_path))
            parse_coords(coords_path, results_dir)


if __name__ == '__main__':

    print(sys.version)
    print(sys.executable)

    # add dir to path so we can import .py files (modules) in there
    sys.path.append('./support_files/')

    # make ./support_files/available_bins.csv if it doesn't exist by running
    # survey_available_bins.py
    if not os.path.exists('./support_files/available_bins.csv'):
        subprocess.check_call(['python',
                               './support_files/survey_available_bins.py'])

    results_dir = './results/mummer_results'
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)

    bins = load_summary()
    print(bins.head())

    # For each bin, use mummer to make a .coords file for each other bin.
    # Do bin A --> bin B, and bin B --> bin A for convenience, even though one
    # result could be enough for both.
    # Do all to all, even though some comparisons are not very meaningful.

    bins_list = bins['bin path'].tolist()
    assert type(bins_list) == list, \
        'bins_list is not a list: {}'.format(bins_list)
    # print('bins_list: {}'.format(bins_list))
    # print('type fo bins_list: {}'.format(type(bins_list)))

    # todo: arguments that specify whether to re-mummer or only parse coords.
    # todo: check whether mummer and/or parse_coords already happened
    # (put in functions above)
    analyze_all_bin_pairs(bins_list, results_dir)
    parse_coords(results_dir)


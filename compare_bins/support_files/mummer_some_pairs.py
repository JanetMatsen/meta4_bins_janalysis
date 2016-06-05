import argparse
import os
import subprocess

import pandas as pd

import mummer_two_bins




def get_all_bin_paths():
    bin_info = pd.read_csv('./support_files/available_bins.csv')
    return bin_info['bin path']


def query_bin_file_to_list(filepath):
    print('load paths at {}'.format(filepath))
    with open(filepath) as f:
        lines = f.read().splitlines()
    return lines


def analyze_bin_pairs(partial_bins_list, results_dir,
                          preserve_existing=True):
    """
    loop over a list of some bin paths, and run MUMMER with every other bin
     as the reference.  Also parses the .coords file.

    :return: nothing to terminal/python but saves files
    """
    reference_bin_paths = get_all_bin_paths()

    for query_bin_path in partial_bins_list:

        # There will be a folder for each bin, and the MUMmer results for all
        # other bins as reference within
        result_sub_dir = mummer_two_bins.strip_off_fasta_suffix(
            os.path.basename(query_bin_path))
        results_dir = results_dir + "/" + result_sub_dir

        print("save result in {}".format(results_dir))

        # loop over all the bins, including itself.
        for ref_bin_path in reference_bin_paths:
            # first check whether the file exists:


            expected_coords_path = \
                mummer_two_bins.file_prefix_from_fata_paths(query_bin_path,
                                                            ref_bin_path,
                                                            results_dir) + \
                '.coords'
            coords_exists = os.path.exists(expected_coords_path)

            # Command to send to shell:
            command = ['python', "./support_files/mummer_two_bins.py",
                      query_bin_path, ref_bin_path, results_dir]

            if preserve_existing:

                if coords_exists:
                    print("not writing over existing mummer results: "
                    "{}".format(expected_coords_path))
                    # don't remake the file if it already exists.
                    continue
                else:
                    # Run mummer_two_bins on the pair of fastas.
                    print('mummer comamnd to run: \n`{}`'.format(
                        ' '.join(command)))
                    subprocess.check_call(command)

            # If we don't care whether the file exists or not, make it
            # fresh every time.
            else:
                subprocess.check_call(command)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Run MUMmer using a subset of query bins, and all of the'
                    'reference bins.')

    parser.add_argument("query_bin_path_list", type=str,
                        help='path to list of paths for query bins')
    parser.add_argument("results_dir", type=str,
                        help='path to save results to')
    parser.add_argument("preserve_existing", type=bool, default=True,
                        help='re-run Mummer even if file exists?')

    args = parser.parse_args()

    print(args)

    query_bins_as_list = query_bin_file_to_list(args.query_bin_path_list)

    analyze_bin_pairs(
        partial_bins_list=query_bins_as_list,
        results_dir=args.results_dir,
        preserve_existing=True)

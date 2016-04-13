import os
import subprocess

import pandas as pd

# Load the summary:

bins = pd.read_csv('support_files/bin_summary.csv')
print(bins.head())

# For each bin, use mummer to make a .coords file for each other bin.
# Do bin A --> bin B, and bin B --> bin A for convenience, even though one
# result could be enough for both.
# Do all to all, even though some comparisons are not very meaningful.

# todo: could do some subset of the groups.
groups = []

bins_list = bins['file name'].tolist()
# print('bins_list: {}'.format(bins_list))
# print('type fo bins_list: {}'.format(type(bins_list)))

results_dir = './mummer_results'
if not os.path.exists(results_dir):
    os.mkdir(results_dir)

def bin_names_to_coords_filepath(bin1, bin2):
    outpath = results_dir
    return outpath + '/' + bin1 + "_to_" + bin2


debug_max_loops = 2
for bin1_name in bins_list:
    debug_max_loops -= 1
    if debug_max_loops <= 0:
        break
    print('bin_1 name: {}'.format(bin1_name))
    bins_to_compare_to = bins_list.copy()

    debug_max_loops2 = 3

    for bin2_name in bins_to_compare_to:

        # set up temp loop limiter
        debug_max_loops2 -= 1
        if debug_max_loops2 <= 0:
            break

        print('     ' + bin2_name)

        # prepare a prefix for mummer to use.
        delta_prefix = bin_names_to_coords_filepath(bin1_name, bin2_name)
        print('.delta file prefix: {}'.format(delta_prefix))

        # print('bins_to_compare_to: {}'.format(bins_to_compare_to))

        # Make the .delta file
        # for now allow mummer to run against itself; this is a control.
        # run these commands:
        subprocess.check_call(
            ['/gscratch/lidstrom/software/MUMmer3.23/nucmer',
            '--prefix={}'.format(delta_prefix),
            './individual_bins/' + bin1_name + '.fasta',
            './individual_bins/' + bin2_name + '.fasta'])

        coords_path = open(delta_prefix + '.coords', 'w')
        print('coords_path: {}'.format(coords_path))
        subprocess.check_call(
            ['/gscratch/lidstrom/software/MUMmer3.23/show-coords',
             '-rcl', str(delta_prefix + '.delta')],
            stdout=coords_path)

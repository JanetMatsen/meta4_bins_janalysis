"""
Run MUMMER on a pair of fasta files, parse the .coords file,  and store
in the specified dir.
"""

import argparse

parser = argparse.ArgumentParser(
    description='Run mummer for a pair of bins, and parse .coords to .tsv.')

parser.add_argument("query_bin_path", type=str, help='path to query bin')
parser.add_argument("reference_bin_path", type=str,
                    help='path to reference bin')
parser.add_argument("result_dir", type=str, help='path to save results to')

# makes a namespace like:
# Namespace(query_bin_path='path1.fna', reference_bin_path='path2.fasta',
# result_dir='.')
args = parser.parse_args()
# Access like  args.query_bin_path


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

if __name__ == '__main__':
    print("Run MUMmer for query {} and reference {}.  \n "
          "Save to {}".format(args.query_bin_path,
                              args.reference_bin_path,
                              args.result_dir))
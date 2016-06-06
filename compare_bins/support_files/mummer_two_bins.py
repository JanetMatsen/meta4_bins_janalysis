"""
Run MUMMER on a pair of fasta files, parse the .coords file,  and store
in the specified dir.
"""

import argparse
import os
import subprocess




def mummer_two_bins(query_bin_path, ref_bin_path, results_dir):
    """
    run mummer on a pairs of bins, given two paths
    """
    # prepare a prefix for mummer to use.
    prefix = file_prefix_from_fata_paths(query_bin_path,
                                         ref_bin_path,
                                         results_dir)
    print('prefix: {}'.format(prefix))
    # dir like ./test/elviz-contigs-1056229.Methylotenera-1 instead of
    results_dir_specific = os.path.dirname(prefix)
    print('results_dir_specific: {}'.format(results_dir_specific))
    bin_a_to_b = os.path.basename(prefix)
    print('bin_a_to_b: {}'.format(bin_a_to_b))
    stderr_dir = results_dir_specific + '/stdout_stderr/'
    print('store stderr and some stdout to: {}'.format(stderr_dir))
    if not os.path.exists(stderr_dir):
        os.makedirs((stderr_dir))
    stderr_prefix = results_dir_specific + '/stdout_stderr/' + bin_a_to_b

    # prepare filename for mummer .delta output.
    delta_prefix = prefix
    print('.delta file prefix: {}'.format(delta_prefix))

    # open a file to dump shell standard out to.
    stdout_nucmer_file = stderr_prefix + ".nucmer.out"
    stderr_nucmer_file = stderr_prefix + ".nucmer.err"
    print("stdout_nucmer_file: {}".format(stdout_nucmer_file))
    print("sterr_nucmer_file: {}".format(stderr_nucmer_file))
    print("dump stdout, stderr to {}, {}".format(stdout_nucmer_file,
                                                 stderr_nucmer_file))
    with open(stdout_nucmer_file, 'w') as out, \
            open(stderr_nucmer_file, 'w') as err:
        # Make the .delta file
        # for now allow mummer to run against itself; this is a control.
        # run these commands:
        # USAGE: nucmer  [options]  <Reference>  <Query>
        # so reference is first, then query.
        nucmer_call = ['/work/software/MUMmer3.23/nucmer',
                       '--prefix={}'.format(delta_prefix),
                       ref_bin_path, query_bin_path]
        print('command to run: \n`{}`'.format(' '.join(nucmer_call)))
        subprocess.check_call(nucmer_call, stdout=out, stderr=err)
        # -o makes a .coords file without running show-coords,
        # but makes the .coords file without coverage columns.

    # show-coords parses the delta alignment output of NUCmer and PROmer, 
    # and displays summary information such as position, percent identity 
    # and so on, of each alignment. It is the most commonly used tool 
    # for analyzing the delta files.
    coords_path = prefix + ".coords"
    stderr_coords_file = stderr_prefix + ".coords.err"
    print("dump stdout, stderr to {}, {}".format(coords_path,
                                                 stderr_coords_file))

    #coords_handle = open(coords_path, 'w')
    #print('coords_path: {}'.format(coords_path))

    with open (coords_path, 'w') as out, open(stderr_coords_file, 'w') as err:
        subprocess.check_call(
            ['/work/software/MUMmer3.23/show-coords',
             '-rcl', str(delta_prefix + '.delta')],
            stdout=out, stderr=err)

def strip_off_fasta_suffix(s):
    """
    e.g. "bin_abc.fasta" --> "bin_abc", or "bin_def.fna" --> "bin_def"

    :param s: string to strip fasta suffix off of
    :return: string without fasta suffix
    """
    print('strip off fasta suffix for {}'.format(s))
    try:
        if ".fasta" in s:
            return s.rstrip("\.fasta")
        elif ".fna" in s:
            return s.rstrip("\.fna")
    except ValueError:
        print("Couldn't strip fasta suffix off of {}".format(s))


def file_prefix_from_fata_paths(query_bin_path, ref_bin_path, results_dir):
    query_name = strip_off_fasta_suffix(os.path.basename(query_bin_path))
    assert query_name is not None, "query name is none: {}".format(query_name)

    ref_name = strip_off_fasta_suffix(os.path.basename(ref_bin_path))
    assert ref_name is not None, "ref name is none: {}".format(query_name)

    return results_dir + '/' + query_name + "_to_" + ref_name


def parse_coords(query_bin_path, ref_bin_path, results_dir):
    """
    write a .tsv file summarising a .coords file made from two bin files.

    :return:None
    """
    # prepare the path to look for
    coords_path = file_prefix_from_fata_paths(query_bin_path,
                                              ref_bin_path,
                                              results_dir) + ".coords"
    # check that .coords file actually exists
    assert(os.path.exists(coords_path)), \
        "path {} doesn't exist".format(coords_path)

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
    print('command to parse .coords: \n`{}`'.format(" ".join(parse_command)))
    subprocess.check_call(parse_command)


if __name__ == '__main__':
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


    print("Run MUMmer for query {} and reference {}.  \n "
          "Save to {}".format(args.query_bin_path,
                              args.reference_bin_path,
                              args.result_dir))

    if not os.path.exists(args.result_dir):
        os.makedirs(args.result_dir)


    coords_path = mummer_two_bins(query_bin_path=args.query_bin_path,
                                  ref_bin_path=args.reference_bin_path,
                                  results_dir=args.result_dir)

    parse_coords(args.query_bin_path,
                 args.reference_bin_path,
                 args.result_dir)

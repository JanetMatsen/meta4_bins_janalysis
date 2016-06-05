"""
Run MUMMER on a pair of fasta files, parse the .coords file,  and store
in the specified dir.
"""

import argparse
import os
import subprocess

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


def mummer_two_bins(query_bin_path, ref_bin_path, results_dir):
    """
    run mummer on a pairs of bins, and return the path to the .coords file
    to be parsed into a .tsv

    :return: the path to the resulting .coords file
    """
    # prepare a prefix for mummer to use.
    delta_prefix = make_coords_prefix(query_bin_path, ref_bin_path, results_dir)
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

    # for convenience, return the path to .coords so we can parse it next
    # without doing more string manipulation.
    return coords_path


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



def make_coords_prefix(query_bin_path, ref_bin_path, results_dir):
    """
    Make a prefix for the .delta file by stripping off .fasta off file names

    Uses the same format as .coords, so
    :param query_bin_path:
    :param ref_bin_path:
    :param results_dir:
    :return:
    """
    query_name = strip_off_fasta_suffix(os.path.basename(query_bin_path))
    assert query_name is not None, "query name is none: {}".format(query_name)

    ref_name = strip_off_fasta_suffix(os.path.basename(ref_bin_path))
    assert ref_name is not None, "ref name is none: {}".format(query_name)

    delta_prefix = \
        bin_names_to_coords_filepath(
            query_bin=query_name,
            ref_bin=ref_name,
            results_dir=results_dir)
    return delta_prefix


def make_coords_path(query_bin_path, ref_bin_path, results_dir):
    delta_prefix = make_coords_prefix(query_bin_path, ref_bin_path, results_dir)
    coords_path = delta_prefix + '.coords'
    return coords_path


def bin_names_to_coords_filepath(query_bin, ref_bin, results_dir):
    """
    prepare a file path for results
    :param query_bin: bin number 1 name/filepath (reference sequence)
    :param ref_bin: bin number 2 name/filepath.  (query sequence)
    :return:string like Acidovora-69x_Ga0081644_to_Acidovorax-79_Ga0081651
    """
    print("use names: {}, {}, {}".format(results_dir, query_bin, ref_bin))
    return results_dir + '/' + query_bin + "_to_" + ref_bin


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





if __name__ == '__main__':
    print("Run MUMmer for query {} and reference {}.  \n "
          "Save to {}".format(args.query_bin_path,
                              args.reference_bin_path,
                              args.result_dir))

    if not os.path.exists(args.result_dir):
        os.makedirs(args.result_dir)


    coords_path = mummer_two_bins(query_bin_path=args.query_bin_path,
                                  ref_bin_path=args.reference_bin_path,
                                  results_dir=args.result_dir)

    parse_coords(coords_path, args.result_dir)
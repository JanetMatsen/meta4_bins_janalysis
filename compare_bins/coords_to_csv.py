#!/usr/bin/env python
# from https://raw.githubusercontent.com/widdowquinn/scripts/master/bioinformatics/nucmer_to_crunch.py
#
# nucmer_to_crunch.py
#
# USAGE: Usage: nucmer_to_crunch.py [-h] [-o OUTFILENAME] [-i INFILENAME] [-v]
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -o OUTFILENAME, --outfile OUTFILENAME
#                         Output .crunch file
#   -i INFILENAME, --infile INFILENAME
#                         Input .coords file
#   -v, --verbose         Give verbose output
#
# A short script that converts the output of MUMmer's show-coords package
# to a .crunch file that can be used in Sanger's ACT comparative genomics
# visualisation tool.
#
# The script acts equivalently to the one-liner:
#
# tail -n +6 in.coords | awk \
# '{print $7" "$10" "$1" "$2" "$12" "$4" "$5" "$13}' > out.crunch
#
#
# but has the advantage that you don't have to remember which columns go in
# which order, and the Python boilerplate provides nicer logging and usage
# information.
#
# Copyright (C) 2014 The James Hutton Institute
# Author: Leighton Pritchard
#
# Contact:
# leighton.pritchard@hutton.ac.uk
#
# Leighton Pritchard,
# Information and Computing Sciences,
# James Hutton Institute,
# Errol Road,
# Invergowrie,
# Dundee,
# DD6 9LH,
# Scotland,
# UK
#
# The MIT License
#
# Copyright (c) 2010-2014 The James Hutton Institute
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

###
# IMPORTS

from argparse import ArgumentParser

import logging
import logging.handlers
import os
import re
import sys


###
# FUNCTIONS

# Parse cmd-line
def parse_cmdline(args):
    """ Parse command-line arguments. Note that the input and output
        directories are positional arguments
    """
    parser = ArgumentParser(prog="nucmer_to_crunch.py")
    parser.add_argument("-o", "--outfile", dest="outfilename",
                        action="store", default=None,
                        help="Output .crunch file")
    parser.add_argument("-i", "--infile", dest="infilename",
                        action="store", default=None,
                        help="Input .coords file")
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action="store_true",
                        help="Give verbose output")
    return parser.parse_args()


# Report last exception as string
def last_exception():
    """ Returns last exception as a string
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return ''.join(traceback.format_exception(exc_type, exc_value,
                                              exc_traceback))


def colname_to_index_list(colname_list):
    """
    Send a list of desied columns such as ['S1', 'COV R'] and get a list
    of the columns corresponding to those data.
    (E.g. [1, 15] for example above)

    :param colname_list: a list of columns whose elements are in
        ['S1', 'E1', 'S2', 'E2', 'LEN1', 'LEN2', '% IDY',
         'LEN R', 'LEN Q', 'COV R', 'COV Q', 'TAGS']
    :return:
    """
    col_dict = {'S1':0, 'E1':1, 'S2':3, 'E2':4, 'LEN1': 6, 'LEN2':7,
                '% IDY':9, 'LEN R':11, 'LEN Q':12, 'COV R':14,
                'COV Q':15, 'TAGS (ref)':17, 'TAGS (query)':18}
    # JM note: the | that divides the columns counts for indexing.
    # 1- 6:    [S1]     [E1]  |     [S2]     [E2]  |
    # 7 - 14:  [LEN 1]  [LEN 2]  |  [% IDY]  |  [LEN R]  [LEN Q]  |
    # 15 - 18: [COV R]  [COV Q]  | [TAGS]
    # [COV R]  = percent alignment coverage in the reference sequence
    # [COV Q] percent alignment coverage in the query sequence
    # [TAGS] = the reference and query FastA IDs respectively
    columns = []
    for cn in colname_list:
        col_num = col_dict[cn]
        columns.append(col_num)
    return columns

# test grabbing of a few columns.

def row_and_indices_to_output_row(row_string, col_indices):
    pass


# Process the input stream
def process_stream(infh, outfh):
    """ Processes the input stream, assuming show-coords output, with
        five header lines, and whitespace separation.

        show-coords output has the following columns (post-processing)

        1: reference sequence start
        2: reference sequence end
        3: subject sequence start
        4: subject sequence end
        5: reference alignment length
        6: subject alignment length
        7: alignment percentage identity
        8: reference sequence ID
        9: subject sequence ID

    """
    # Read in the input stream into a list of lines
    try:
        tbldata = list(infh.readlines())
    except:
        logger.error("Could not process input (exiting)")
        logger.error(last_exception())
        sys.exit(1)
    logger.info("Read %d lines from input" % len(tbldata))

    header_row = tbldata[3]
    tbldata = tbldata[5:]
    logger.info("Skipped header lines.")

    # check that I have the header stuff right.
    print(header_row)
    cols = header_row.split()
    #print(cols)
    #print("------")
    #print(re.findall(r"\[([A-z ]+)\]", header_row))

    # save header to file


    print_lines = 10
    for line in [l.strip().split() for l in tbldata if
                 len(l.strip())]:
        print_lines -= 1
        if print_lines == 0:
            return
        # Due to the column marker symbols, there are offsets for the
        # columns, relative to those in the text above.

        #   col_dict = {'S1':1, 'E1':2, 'S2':4, 'E2':5, 'LEN1': 7, 'LEN2':8,
        #               '% IDY':10, 'LEN R':12, 'LEN Q':13, 'COV R':15,
        #               'COV Q':16, 'TAGS (ref)':18, 'TAGS (query)':19}
        cols = ['TAGS (ref)', 'TAGS (query)', 'LEN R',
        #cols = ['S1', 'LEN R',
                'LEN Q', 'COV R', 'COV Q']
        col_indices = colname_to_index_list(cols)
        print('col_indices: {}'.format(col_indices))
        values = [line[i] for i in col_indices]

        output_line = "\t".join(values)

        print(output_line)

        # outfh.write(' '.join([line[6],  # LEN1
        #                       line[9],  # % IDY
        #                       line[0],  # S1
        #                       line[1],  # E1
        #                       line[11], # LEN Q
        #                       line[3],  # S2
        #                       line[4],  # E2
        #                       line[12]]) # LEN Q
        #             + '\n')


###
# SCRIPT

if __name__ == '__main__':

    # Parse command-line
    args = parse_cmdline(sys.argv)

    # We set up logging, and modify loglevel according to whether we need
    # verbosity or not
    logger = logging.getLogger('nucmer_to_crunch.py')
    logger.setLevel(logging.DEBUG)
    err_handler = logging.StreamHandler(sys.stderr)
    err_formatter = logging.Formatter('%(levelname)s: %(message)s')
    err_handler.setFormatter(err_formatter)
    if args.verbose:
        err_handler.setLevel(logging.INFO)
    else:
        err_handler.setLevel(logging.WARNING)
    logger.addHandler(err_handler)

    # Report arguments, if verbose
    logger.info(args)

    # Do we have an input file?  No? Then use stdin
    if args.infilename is None:
        infhandle = sys.stdin
        logger.info("Using stdin for input")
    else:
        logger.info("Using %s for input" % args.infilename)
        try:
            infhandle = open(args.infilename, 'rU')
        except:
            logger.error("Could not open input file: %s (exiting)" %
                         args.infilename)
            logger.error(''.join(
                traceback.format_exception(sys.last_type,
                                           sys.last_value,
                                           sys.last_traceback)))
            sys.exit(1)

    # Do we have an output file?  No? Then use stdout
    if args.outfilename is None:
        outfhandle = sys.stdout
        logger.info("Using stdout for output")
    else:
        logger.info("Using %s for output" % args.outfilename)
        try:
            outfhandle = open(args.outfilename, 'w')
        except:
            logger.error("Could not open output file: %s (exiting)" %
                         args.outfilename)
            logger.error(''.join(
                traceback.format_exception(sys.last_type,
                                           sys.last_value,
                                           sys.last_traceback)))
            sys.exit(1)

    # Process input stream
    process_stream(infhandle, outfhandle)
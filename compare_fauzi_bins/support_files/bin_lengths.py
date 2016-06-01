import glob
import re

from Bio import SeqIO
import pandas as pd


BIN_PATH = './individual_bins/'
RESULT_PATH = './support_files/'


def bin_base_pairs(filepath):
    """
    Though most of the sample info comes from summarise_bins.py,
    this adds a final column back on

    :param filepath:
    :return:
    """
    bp = 0
    contigs = 0
    for seq_record in SeqIO.parse(filepath, "fasta"):
        bp += len(seq_record)
        contigs += 1
    return {'contigs':contigs, 'bp':bp}


def extract_bin_number(string):
    # Ga0081607_1001 --> Ga0081607
    m = re.search("(Ga[0-9]+)", string)
    assert m, 'no match found in {}'.format(string)
    return m.group(1)


def walk_bins():
    results = pd.DataFrame()
    global BIN_PATH
    print(BIN_PATH)
    for bin_path in glob.glob(BIN_PATH + '*.fasta'):
        filename = re.search('([A-Za-z0-9_-]+.fasta)', bin_path).group(0)
        print(bin_path)
        print(filename)
        # Get a dict of info about contigs, bp
        stats = bin_base_pairs(bin_path)
        print(stats)
        df_row = pd.DataFrame({k:[v] for k, v in stats.items()})
        # add on bin filename:
        df_row['file name'] = filename
        # add on a bin number.
        df_row['bin'] = extract_bin_number(filename)
        if results.empty:
            print('start new dataframe')
            results = df_row
        else:
            print('append')
            results = results.append(df_row)
        print("")
    return results


if __name__ == '__main__':
    summary = walk_bins()
    summary.to_csv(RESULT_PATH + 'bin_stats.tsv', sep = '\t', index=False)


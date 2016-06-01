import re

import pandas as pd


def extract_contig_ID(string):
    # 1:>Ga0081607_1001 [organism=Methylobac... --> Ga0081607_1001
    return re.search("Ga[0-9]+_[0-9]+", string).group(0)


def extract_contig_number(string):
    # Ga0081607_1001 --> 1001
    return re.search("Ga[0-9]+_([0-9]+)", string).group(1)


def extract_bin_number(string):
    # Ga0081607_1001 --> Ga0081607
    # Todo: merge with support_files.bin_lengths.extract_bin_number
    m = re.search("(Ga[0-9]+)_[0-9]+", string)
    assert m, 'no match found in {}'.format(string)
    return m.group(1)


def extract_common_name(string):
    # [organism=Methylophilus methylotrophus-127-1 (UID203)]
    # --> Methylophilus methylotrophus-127-1
    # need to escape the brackets or I get a unbalanced parentheses warning.
    return re.search("\[organism=([\w\s-]+) \(UID[0-9]+\)\]", string).group(1)


def prepare_summary_df(filepath="./DNA_names.txt"):
    df = pd.read_csv(filepath, sep='\t', names=['row name'])
    # Extract the contig name (e.g. Ga0081607_1001)
    df['contig ID'] = df['row name'].apply(extract_contig_ID)
    df['contig number'] = df['contig ID'].apply(extract_contig_number)
    df['bin'] = df['contig ID'].apply(extract_bin_number)
    df['name'] = df['row name'].apply(extract_common_name)
    return df


def summarise_df(df):
    summary = df[['bin', 'name']].drop_duplicates().reset_index()[['bin',
                                                                   'name']]
    # get the contig counts
    num_contigs_in_bins = pd.DataFrame(
        df[['bin', 'contig number']].groupby(
            'bin')['contig number'].count().reset_index())
    num_contigs_in_bins.rename(columns={'contig number': 'contig count'},
                               inplace=True)
    summary = pd.merge(summary, num_contigs_in_bins)
    # prepare file names
    names = summary['name'] + '_' + summary['bin']
    names = names.map(lambda x: x.replace(" ", "_"))
    summary['bin name'] = names
    return summary


if __name__ == "__main__":
    print('summarise bins with summarise_bins.py')
    bins = prepare_summary_df('./support_files/DNA_names.txt') 
    bin_summary = summarise_df(bins).sort_values('name')
    # todo: make more flexible.  Use OS to get cwd?  Command line arg?  
    bin_summary.to_csv('./support_files/bin_summary.csv', index=False)

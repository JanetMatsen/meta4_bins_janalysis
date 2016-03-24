import matplotlib as mpl
mpl.use('Agg')

import glob
import re

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import seaborn as sns

import unused_reads as ur




mpl.rcParams.update({
    'font.size': 16, 'axes.titlesize': 17, 'axes.labelsize': 15,
    'xtick.labelsize': 13,
    'ytick.labelsize': 13,
    'font.weight': 600,
    'axes.labelweight': 600, 'axes.titleweight': 600,
    'figure.autolayout': True})


def read_blasted(dirname):
    """
    read in all of the blasted .tsv files in a specified directory and merge
    them into one dataframe.  Adds a column for the sample name and one for the
    downsampling granularity.

    :param dirname: path to blasted files
    :return: pandas dataframe containing all files.
    """
    path = dirname
    all_files = glob.glob(path + "/*.tsv")
    print(all_files)
    frame = pd.DataFrame()
    list_ = []
    df_dtypes = {}
    for file_ in all_files:
        df = pd.read_csv(file_, sep='\t', dtype=df_dtypes)
        df['sample'] = re.search(r'[0-9]+_[HL]OW[0-9]+', file_).group(0)
        df['downsample granularity'] = \
            int(re.search(r'[0-9]+_[HL]OW[0-9]+_(['r'0-9]+)', file_).group(1))
        # append on a column that says which file it is.
        list_.append(df)
    frame = pd.concat(list_)
    return frame


def subset_to_downsample_granularity(df, downsample_granularity):
    # subset df to the downsampling level
    print("available downsampling granularities: {}".format(
        df['downsample granularity'].unique()))
    df = df[df['downsample granularity'] == downsample_granularity]
    # check that the dataframe isn't empty
    assert df.shape[0] > 0, 'dataframe is empty for downssample_granularity ' \
                            '= {}'.format(downsample_granularity)
    return df


def plot_results(df, data_name, downsample_granularity):
    df = subset_to_downsample_granularity(df, downsample_granularity)

    plot_length_dist(df,
                     data_name + "_ds_{}".format(downsample_granularity),
                     PLOT_DIR)
    plot_pident_dist(df,
                     data_name + "_ds_{}".format(downsample_granularity),
                     PLOT_DIR)
    plot_e_score_dist(df,
                      data_name + "_ds_{}".format(downsample_granularity),
                      PLOT_DIR)
    pass


def plot_length_dist(df, data_name, filepath):
    fig, ax = plt.subplots(1, 1) # figsize=(5, 6))
    sns.despine()  # Removes the boxes around the plots.
    plot_data = df.length
    plot_data.plot.hist(ax=ax)
    ax.set_title('Distributions of BLAST lengths: {}'.format(data_name),
                 y=1.05)
    ax.set_xlabel('length of BLAST alignment')
    ax.figure.savefig(filepath + data_name + "_lengths" + '.pdf')
    return ax


def plot_pident_dist(df, data_name, filepath):
    fig, ax = plt.subplots(1, 1) # figsize=(5, 6))
    sns.despine()  # Removes the boxes around the plots.
    plot_data = df.pident
    plot_data.plot.hist(ax=ax)
    ax.set_title('Distributions percent identity: {}'.format(data_name),
                 y=1.05)
    ax.set_xlabel('percent identity (pident)')
    ax.figure.savefig(filepath + data_name + "_pident" + '.pdf')
    return ax


def plot_e_score_dist(df, data_name, filepath):
    # The Expect value (E) is a parameter that describes the number of hits
    # one can "expect" to see by chance when searching a database of a
    # particular size. It decreases exponentially as the Score (S) of the
    # match increases. Essentially, the E value describes the random
    # background noise. For example, an E value of 1 assigned to a hit can be
    # interpreted as meaning that in a database of the current size one might
    # expect to see 1 match with a similar score simply by chance.

    # The lower the E-value, or the closer it is to zero, the more
    # "significant" the match is. However, keep in mind that virtually
    # identical short alignments have relatively high E values. This is
    # because the calculation of the E value takes into account the length of
    # the query sequence. These high E values make sense because shorter
    # sequences have a higher probability of occurring in the database purely
    # by chance. For more details please see the calculations in the BLAST
    # Course: http://www.ncbi.nlm.nih.gov/BLAST/tutorial/Altschul-1.html
    fig, ax = plt.subplots(1, 1) # figsize=(5, 6))
    sns.despine()  # Removes the boxes around the plots.
    plot_data = df.evalue
    MIN, MAX = min(plot_data), max(plot_data)
    plot_data.plot.hist(ax=ax, bins=10**np.linspace(np.log10(MIN), np.log10(MAX), 50))
    ax.set_xscale('log')
    ax.set_title('Distributions e values: {}'.format(data_name), y=1.05)
    ax.set_xlabel('e-value')
    ax.figure.savefig(filepath + data_name + "_e_value" + '.pdf')
    return ax


def summarise(df, min_pident, min_length, downsample_granularity):
    # filter by length (start with >140).  Reads are 150 long.
    # filter by % identity.  Start with 90%.  May bump down to 85%.

    # subset on the granularity desired:
    df = subset_to_downsample_granularity(df, downsample_granularity)

    # trim off the low percent identity rows:
    num_rows_before = df.shape[0]
    df = df[df['pident'] >= min_pident]
    num_rows_after = df.shape[0]
    print('fraction of rows removed for min percent_identity = {}: {}'.format(
        min_pident, (num_rows_after*1.0/num_rows_before) * 100))

    # trim off the low length matches:
    num_rows_before = df.shape[0]
    df = df[df['length'] >= min_length]
    num_rows_after = df.shape[0]
    print('fraction of rows removed for min length = {}: {}'.format(
        min_length, (num_rows_after*1.0/num_rows_before)*100))

    # count frequency of each hit (stitle) for each sample

    # Save to csv(s).  One file per sample?  And one with everything?
    # Make separate dir for results.
    return df


def run_analysis(path='../../unused_reads', make_plots=True):
    unmapped = read_blasted(path + '/unmapped-final/blast_results/')
    unspecific = \
        read_blasted(path + '/multiply_mapped-final/blast_results/')
    # Make plots
    if make_plots:
        plot_results(unmapped, 'unmapped--all', downsample_granularity=10000)
        plot_results(unspecific, 'unspecific--all', downsample_granularity=100)
    return {'unspecific': unspecific, 'unmapped': unmapped}


if __name__ == "__main__":
    PLOT_DIR = 'plots/'
    ur.create_dir(PLOT_DIR)
    run_analysis(path='./')

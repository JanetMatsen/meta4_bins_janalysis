import glob
import re

import matplotlib.pyplot as plt
import matplotlib as mpl

import pandas as pd
import seaborn as sns

import unused_reads as ur

PLOT_DIR = '../../unused_reads/plots/'
ur.create_dir(PLOT_DIR)


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
    for file_ in all_files:
        df = pd.read_csv(file_, sep='\t')
        df['sample']= re.search(r'[0-9]+_[HL]OW[0-9]+', file_).group(0)
        df['downsample granularity']= re.search(r'[0-9]+_[HL]OW[0-9]+_([0-9]+)', file_).group(1)
        # append on a column that says which file it is.
        list_.append(df)
    frame = pd.concat(list_)
    return frame


def plot_results(df, data_name):
    plot_length_dist(df, data_name, PLOT_DIR)
    plot_pident_dist(df, data_name, PLOT_DIR)
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

unmapped = read_blasted('../../unused_reads/unmapped-final/blast_results/')
# Make plots
plot_results(unmapped, 'unmapped--all')

unspecific = \
    read_blasted('../../unused_reads/multiply_mapped-final/blast_results/')
# Make plots
plot_results(unspecific, 'unspecific--all')


def most_common_stitiles(min_pid, min_length):
    # TODO: write a function that summarises the most frequent stitle values
    # ?? Break apart by sample?
    # first trim off min percent identity
    # then trim off by the minimum length
    pass


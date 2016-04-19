import numpy as np
import sys

import pandas as pd

sys.path.append('./support_files/')
import summarise_bins


def load_individual_bin_summaries():
    return pd.read_csv('support_files/bin_summary.csv')


def load_one_mummer_result(filepath):
    # trim ./mummer-results/filename.tsv to filename.tsv
    df = pd.read_csv(filepath, sep='\t')
    # The 2 argument says split at most 2 times.
    df['mummer file'] = filepath.split("/", 2)[2]
    df['ref bin'] = df['TAGS (ref)'].apply(
        lambda x: summarise_bins.extract_bin_number(x))
    df['query bin'] = df['TAGS (query)'].apply(
        lambda x: summarise_bins.extract_bin_number(x))
    df['ref contig'] = df['TAGS (ref)'].apply(
        lambda x: summarise_bins.extract_contig_number(x))
    df['query contig'] = df['TAGS (query)'].apply(
        lambda x: summarise_bins.extract_contig_number(x))
    return df


def prep_summary_for_merge(df, prepend_string):
    df2 = df.copy()
    df2.columns = map(lambda x: prepend_string + x, df.columns)
    return df2


def prepare_result(filepath):
    result = load_one_mummer_result(filepath)
    # prepare meta-info for the query bin
    query_metainfo = prep_summary_for_merge(
        df=load_individual_bin_summaries(),
        prepend_string='query ')
    # prepare meta-info for the ref bin
    ref_metainfo = prep_summary_for_merge(
        df=load_individual_bin_summaries(),
        prepend_string='ref ')
    result = pd.merge(result, query_metainfo)
    result = pd.merge(result, ref_metainfo)
    return result


def filename_to_title(filename):
    # "abc_to_def" --> "abc \n to def"
    # strip off .tsv
    filename = filename.rstrip('\.tsv')
    bin_list = filename.split("_to_")
    title = '{} \n to {}'.format(bin_list[0], bin_list[1])
    return title


def plot_IDY_vs_len(filepath, save_path='./plots/'):
    df = load_one_mummer_result(filepath)
    if df.shape[0] > 1:
        plot = df.plot.scatter(x='LEN 2', y='% IDY')
        filename = df['mummer file'][0]
        plot.set_title(filename_to_title(filename), y=1.05)
        if save_path:
            save_path = save_path + filename.rstrip('.tsv') + '.pdf'
            plot.figure.savefig(save_path, bbox_inches='tight')


def percent_identity(dataframe):
    # get a dataframe that has one row per reference contig, and the
    # corresponding longest length
    keeper_rows_df = dataframe.groupby('TAGS (query)')['LEN 2'].agg(
        np.max).reset_index()
    # merge this dataframe onto the main dataframe to get the rows with the
    # longest matches.
    longest_rows = pd.merge(dataframe, keeper_rows_df)
    # calculate the length-weighted percent identiy, known as ANI.
    percent_ident = \
        sum(longest_rows['% IDY']*longest_rows['LEN 2'])*1./\
        longest_rows['LEN 2'].sum()
    return percent_ident


def summarise_all_mummer_results(filepath_list):
    # loop over all the .tsv files, and run filename_to_summary
    # merge individual summaries into an umbrella pandas
    # include a file path to that bin.
    # merge on the info about the individual bins
    # return summary dataframe.
    pass


def load_all_mumer_results():
    pass

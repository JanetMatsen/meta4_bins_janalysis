import glob
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


def plot_identity_vs_len(filepath, save_path='./plots/'):
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
    # if there are zero rows, return zero similarity
    if keeper_rows_df.shape[0] == 0:
        print('no rows for {}; assume zero similarity'.format(filepath))
        return 0
    # merge this dataframe onto the main dataframe to get the rows with the
    # longest matches.
    longest_rows = pd.merge(dataframe, keeper_rows_df)
    # calculate the length-weighted percent identiy, known as ANI.
    percent_ident = \
        sum(longest_rows['% IDY']*longest_rows['LEN 2'])*1. / \
        longest_rows['LEN 2'].sum()
    return percent_ident


def percent_idty_all_results(filepath_list):
    num_empty = 0
    num_with_contents = 0
    summary_all_samples = pd.DataFrame()
    for filepath in filepath_list:
        #print('analyze {}'.format(filepath))
        # load the dataframe for that file path
        single_result = prepare_result(filepath)
        # make a dataframe with the meta info
        summary = single_result[['mummer file', 'ref bin', 'query bin',
                                 'query name', 'query contig count',
                                 'query bin name', 'ref name',
                                 'ref contig count', 'ref bin name']]
        if summary.shape[0] == 0:
            print('{} has zero rows; omit it from summary'.format(filepath))
            num_empty += 1
            continue
        else:
            print('--> {}:'.format(filepath))
            num_with_contents += 1
        # calculate % identity for each file
        p_id = percent_identity(single_result)
        summary['% identity'] = p_id
        # print('result sample: \n {}'.format(summary.head(3)))
        # merge on the first row of the repetitive result dataframe
        # if no percent_identities dataframe exists (shouldn't on first
        # loop), then make one.
        if summary_all_samples.empty:
            summary_all_samples = summary.head(1)
            print('shape: {}'.format(summary_all_samples.shape))
        else:
            summary_all_samples = summary_all_samples.append(summary.head(1))
            print('shape: {}'.format(summary_all_samples.shape))

    print('number of empty and filled files: {}, {}'.format(
        num_empty, num_with_contents
    ))
    return summary_all_samples

    # merge individual summaries into an umbrella pandas
    # include a file path to that bin.
    # merge on the info about the individual bins
    # return summary dataframe.
    pass


def pivot_identity_table(identity_table):
    identity_table = identity_table.pivot(
        index='query name', columns='ref name', values='% identity')
    identity_table.fillna(value=0, inplace=True)
    return identity_table


def pivot_saved_tsv(saved_tsv_path, out_path):
    df = pd.read_csv(saved_tsv_path, sep='\t')
    df = pivot_identity_table(df)
    df.to_csv(out_path, sep='\t')


def plot_heatmap(pivoted_table):
    plot = sns.heatmap(res_piv)
    return plot


if __name__ == "__main__":
    test_samples = glob.glob('./mummer_results/*.tsv')
    i_res = percent_idty_all_results(test_samples)
    print('len of test_samples: {}'.format(len(test_samples)))
    print('len of test_samples set: {}'.format(
        len(set(test_samples))))
    unpivoted_path = 'percent_identities.tsv'
    i_res.to_csv(unpivoted_path, sep='\t')
    # pivot for seaborn plotting
    pivoted_path = 'percent_identities--pivoted.tsv'
    pivot_saved_tsv(unpivoted_path, pivoted_path)
